package server

import (
	"crypto/subtle"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"heuser27/internal/ingest"
)

func (s *Server) handleAdminMe(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]bool{"authenticated": s.isAdmin(r)})
}

func (s *Server) handleAdminLogin(w http.ResponseWriter, r *http.Request) {
	var body struct {
		Password string `json:"password"`
	}
	if err := json.NewDecoder(io.LimitReader(r.Body, 4096)).Decode(&body); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}
	if subtle.ConstantTimeCompare([]byte(body.Password), []byte(s.AdminPassword)) != 1 {
		writeError(w, http.StatusUnauthorized, "incorrect admin password")
		return
	}
	http.SetCookie(w, &http.Cookie{
		Name:     "heuser27_admin",
		Value:    s.signAdminToken(),
		Path:     "/",
		HttpOnly: true,
		SameSite: http.SameSiteLaxMode,
		MaxAge:   86400 * 7,
	})
	writeJSON(w, http.StatusOK, map[string]bool{"authenticated": true})
}

func (s *Server) handleAdminLogout(w http.ResponseWriter, r *http.Request) {
	http.SetCookie(w, &http.Cookie{
		Name:     "heuser27_admin",
		Value:    "",
		Path:     "/",
		HttpOnly: true,
		SameSite: http.SameSiteLaxMode,
		MaxAge:   -1,
	})
	writeJSON(w, http.StatusOK, map[string]bool{"authenticated": false})
}

type AdminMatrixCell struct {
	SubmissionID   string `json:"submission_id"`
	HWNumber       int    `json:"hw_number"`
	SubmittedAt    string `json:"submitted_at"`
	PrimaryURL     string `json:"primary_url"`
	SecondaryURL   string `json:"secondary_url"`
	EmbedURL       string `json:"embed_url"`
	Playable       bool   `json:"playable"`
	IsLocalOnlyURL bool   `json:"is_local_only_url"`
	AttemptCount   int    `json:"attempt_count"`
	Votes          int    `json:"votes"`
	CommentCount   int    `json:"comment_count"`
}

func (s *Server) handleAdminSummary(w http.ResponseWriter, r *http.Request) {
	students, err := s.Store.ListStudents(true)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	homeworks, err := s.Store.ListHomeworks()
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	matrix, err := s.buildSubmissionMatrix()
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	comments, err := s.Store.ListComments("", "", true)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	syncLogs, err := s.Store.RecentSyncLogs()
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"students":  students,
		"homeworks": homeworks,
		"matrix":    matrix,
		"comments":  comments,
		"sync_logs": syncLogs,
	})
}

func (s *Server) buildSubmissionMatrix() (map[string]map[int]AdminMatrixCell, error) {
	rows, err := s.Store.DB.Query(`
		SELECT sub.id, sub.student_id, sub.hw_number, sub.submitted_at,
		       sub.primary_url, sub.secondary_url, sub.embed_url,
		       sub.playable, sub.is_local_only_url, sub.attempt_count,
		       (SELECT COUNT(*) FROM votes v WHERE v.submission_id = sub.id) AS vote_cnt,
		       (SELECT COUNT(*) FROM comments c WHERE c.submission_id = sub.id) AS cmt_cnt
		FROM submissions sub
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	matrix := make(map[string]map[int]AdminMatrixCell)
	for rows.Next() {
		var sid string
		var cell AdminMatrixCell
		var playable, localOnly int
		if err := rows.Scan(
			&cell.SubmissionID, &sid, &cell.HWNumber, &cell.SubmittedAt,
			&cell.PrimaryURL, &cell.SecondaryURL, &cell.EmbedURL,
			&playable, &localOnly, &cell.AttemptCount,
			&cell.Votes, &cell.CommentCount,
		); err != nil {
			return nil, err
		}
		cell.Playable = playable == 1
		cell.IsLocalOnlyURL = localOnly == 1
		if matrix[sid] == nil {
			matrix[sid] = make(map[int]AdminMatrixCell)
		}
		matrix[sid][cell.HWNumber] = cell
	}
	return matrix, rows.Err()
}

func (s *Server) handleAdminStar(w http.ResponseWriter, r *http.Request) {
	var body struct {
		StudentID string `json:"student_id"`
		Starred   bool   `json:"starred"`
		StarNote  string `json:"star_note"`
	}
	if err := json.NewDecoder(io.LimitReader(r.Body, 4096)).Decode(&body); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}
	if strings.TrimSpace(body.StudentID) == "" {
		writeError(w, http.StatusBadRequest, "student_id required")
		return
	}
	if err := s.Store.SetStudentStar(body.StudentID, body.Starred, strings.TrimSpace(body.StarNote)); err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"student_id": body.StudentID,
		"starred":    body.Starred,
		"star_note":  strings.TrimSpace(body.StarNote),
	})
}

func (s *Server) handleAdminResync(w http.ResponseWriter, r *http.Request) {
	s.SyncMu.Lock()
	defer s.SyncMu.Unlock()

	res, err := ingest.SyncAll(s.Store, s.BaseDir, s.DataDir, "admin-resync")
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	writeJSON(w, http.StatusOK, res)
}

func (s *Server) handleAdminUploadXlsx(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseMultipartForm(32 << 20); err != nil {
		writeError(w, http.StatusBadRequest, "invalid multipart upload")
		return
	}
	hwStr := strings.TrimSpace(r.FormValue("hw_number"))
	hwNum, err := strconv.Atoi(hwStr)
	if err != nil || hwNum < 1 || hwNum > 30 {
		writeError(w, http.StatusBadRequest, "invalid hw_number (1-30)")
		return
	}
	file, header, err := r.FormFile("file")
	if err != nil {
		writeError(w, http.StatusBadRequest, "missing .xlsx file")
		return
	}
	defer file.Close()

	if !strings.HasSuffix(strings.ToLower(header.Filename), ".xlsx") {
		writeError(w, http.StatusBadRequest, "only .xlsx files are accepted")
		return
	}

	destDir := filepath.Join(s.DataDir, "uploads", fmt.Sprintf("hw%d", hwNum))
	if err := os.MkdirAll(destDir, 0o755); err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}

	// Keep the uploaded file with timestamp prefix so it becomes the newest .xlsx for that HW
	safeName := filepath.Base(header.Filename)
	destPath := filepath.Join(destDir, fmt.Sprintf("%d_%s", time.Now().Unix(), safeName))
	out, err := os.Create(destPath)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	if _, err := io.Copy(out, io.LimitReader(file, 25<<20)); err != nil {
		_ = out.Close()
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	_ = out.Close()

	s.SyncMu.Lock()
	res, syncErr := ingest.SyncAll(s.Store, s.BaseDir, s.DataDir, fmt.Sprintf("admin-upload-hw%d:%s", hwNum, safeName))
	s.SyncMu.Unlock()
	if syncErr != nil {
		writeError(w, http.StatusBadRequest, "failed to parse uploaded xlsx: "+syncErr.Error())
		return
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"uploaded": safeName,
		"hw":       hwNum,
		"sync":     res,
	})
}

func (s *Server) handleAdminDeleteComment(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		writeError(w, http.StatusBadRequest, "invalid comment id")
		return
	}
	if err := s.Store.DeleteComment(id); err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	writeJSON(w, http.StatusOK, map[string]bool{"deleted": true})
}

func (s *Server) handleAdminExportCSV(w http.ResponseWriter, r *http.Request) {
	students, err := s.Store.ListStudents(true)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	homeworks, err := s.Store.ListHomeworks()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	matrix, err := s.buildSubmissionMatrix()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/csv; charset=utf-8")
	w.Header().Set("Content-Disposition", `attachment; filename="heuser27_submissions_summary.csv"`)

	cw := csv.NewWriter(w)
	header := []string{"Student ID", "Name", "Batch", "Status", "Starred", "Submitted Count", "Total Votes"}
	for _, hw := range homeworks {
		header = append(header, fmt.Sprintf("HW%d", hw.HWNumber))
	}
	_ = cw.Write(header)

	for _, st := range students {
		row := []string{
			st.ID,
			st.Name,
			st.Batch,
			st.EnrollmentStatus,
			strconv.FormatBool(st.Starred),
			strconv.Itoa(st.SubmissionCount),
			strconv.Itoa(st.TotalVotes),
		}
		cells := matrix[st.ID]
		for _, hw := range homeworks {
			if c, ok := cells[hw.HWNumber]; ok {
				if c.PrimaryURL != "" {
					row = append(row, c.PrimaryURL)
				} else {
					row = append(row, "Submitted")
				}
			} else {
				row = append(row, "")
			}
		}
		_ = cw.Write(row)
	}
	cw.Flush()
}
