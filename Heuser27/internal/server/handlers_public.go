package server

import (
	"archive/zip"
	"encoding/json"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sort"
	"strings"

	"heuser27/internal/db"
)

type ShowcaseResponse struct {
	Homeworks []db.HomeworkMeta `json:"homeworks"`
	Students  []db.Student      `json:"students"`
	Stats     ShowcaseStats     `json:"stats"`
}

type ShowcaseStats struct {
	TotalStudents    int `json:"total_students"`
	TotalSubmissions int `json:"total_submissions"`
	TotalVotes       int `json:"total_votes"`
	TotalComments    int `json:"total_comments"`
	PlayableGames    int `json:"playable_games"`
	StarredStudents  int `json:"starred_students"`
}

func (s *Server) handleShowcase(w http.ResponseWriter, r *http.Request) {
	homeworks, err := s.Store.ListHomeworks()
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	students, err := s.Store.ListStudents(false)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}

	// Sort: Starred first (by StarredAt desc or Votes desc), then by Votes desc, then SubmissionCount desc, then Name asc
	sort.SliceStable(students, func(i, j int) bool {
		a, b := students[i], students[j]
		if a.Starred != b.Starred {
			return a.Starred
		}
		if a.TotalVotes != b.TotalVotes {
			return a.TotalVotes > b.TotalVotes
		}
		if a.SubmissionCount != b.SubmissionCount {
			return a.SubmissionCount > b.SubmissionCount
		}
		return a.Name < b.Name
	})

	var stats ShowcaseStats
	stats.TotalStudents = len(students)
	for _, st := range students {
		stats.TotalSubmissions += st.SubmissionCount
		stats.TotalVotes += st.TotalVotes
		stats.TotalComments += st.TotalComments
		stats.PlayableGames += st.PlayableCount
		if st.Starred {
			stats.StarredStudents++
		}
	}

	writeJSON(w, http.StatusOK, ShowcaseResponse{
		Homeworks: homeworks,
		Students:  students,
		Stats:     stats,
	})
}

func (s *Server) handleGetStudent(w http.ResponseWriter, r *http.Request) {
	sid := strings.TrimSpace(r.PathValue("id"))
	if sid == "" {
		writeError(w, http.StatusBadRequest, "missing student id")
		return
	}
	ip := clientIP(r)
	student, subs, err := s.Store.GetStudent(sid, ip)
	if err != nil {
		writeError(w, http.StatusNotFound, "student not found")
		return
	}
	comments, err := s.Store.ListComments(sid, "", false)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	if comments == nil {
		comments = []db.Comment{}
	}
	if subs == nil {
		subs = []db.Submission{}
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"student":     student,
		"submissions": subs,
		"comments":    comments,
	})
}

func (s *Server) handleToggleVote(w http.ResponseWriter, r *http.Request) {
	var body struct {
		SubmissionID string `json:"submission_id"`
	}
	if err := json.NewDecoder(io.LimitReader(r.Body, 4096)).Decode(&body); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}
	body.SubmissionID = strings.TrimSpace(body.SubmissionID)
	if body.SubmissionID == "" {
		writeError(w, http.StatusBadRequest, "submission_id is required")
		return
	}
	ip := clientIP(r)
	voted, total, err := s.Store.ToggleVote(body.SubmissionID, ip)
	if err != nil {
		writeError(w, http.StatusNotFound, "submission not found")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"submission_id": body.SubmissionID,
		"voted":         voted,
		"votes":         total,
	})
}

func (s *Server) handleAddComment(w http.ResponseWriter, r *http.Request) {
	var body struct {
		SubmissionID string `json:"submission_id"`
		AuthorName   string `json:"author_name"`
		Body         string `json:"body"`
	}
	if err := json.NewDecoder(io.LimitReader(r.Body, 8192)).Decode(&body); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}
	subID := strings.TrimSpace(body.SubmissionID)
	author := strings.TrimSpace(body.AuthorName)
	text := strings.TrimSpace(body.Body)

	if subID == "" || text == "" {
		writeError(w, http.StatusBadRequest, "submission_id and comment text are required")
		return
	}
	if author == "" {
		author = "Visitor"
	}
	if len(author) > 50 {
		author = author[:50]
	}
	if len(text) > 800 {
		writeError(w, http.StatusBadRequest, "comment must be 800 characters or fewer")
		return
	}

	ip := clientIP(r)
	c, err := s.Store.AddComment(subID, author, text, ip)
	if err != nil {
		status := http.StatusBadRequest
		if strings.Contains(err.Error(), "rate limit") {
			status = http.StatusTooManyRequests
		}
		writeError(w, status, err.Error())
		return
	}
	writeJSON(w, http.StatusCreated, map[string]any{"comment": c})
}

func (s *Server) handleGetLocalFile(w http.ResponseWriter, r *http.Request) {
	rel := strings.TrimSpace(r.URL.Query().Get("path"))
	if rel == "" {
		writeError(w, http.StatusBadRequest, "missing path")
		return
	}
	cleanRel := filepath.Clean(filepath.FromSlash(rel))
	if strings.HasPrefix(cleanRel, "..") || filepath.IsAbs(cleanRel) {
		writeError(w, http.StatusForbidden, "invalid path")
		return
	}
	// Only permit files inside Homework * directories and disallow .xlsx spreadsheets
	low := strings.ToLower(filepath.ToSlash(cleanRel))
	if !strings.HasPrefix(low, "homework ") || strings.HasSuffix(low, ".xlsx") {
		writeError(w, http.StatusForbidden, "access restricted")
		return
	}

	abs := filepath.Join(s.BaseDir, cleanRel)
	if !strings.HasPrefix(filepath.Clean(abs), filepath.Clean(s.BaseDir)) {
		writeError(w, http.StatusForbidden, "forbidden")
		return
	}

	if r.URL.Query().Get("download") == "1" {
		w.Header().Set("Content-Disposition", `attachment; filename="`+filepath.Base(abs)+`"`)
		http.ServeFile(w, r, abs)
		return
	}

	// If zip, return JSON preview of text/md files inside it
	if strings.HasSuffix(low, ".zip") {
		entries, err := readZipTextPreview(abs)
		if err != nil {
			writeError(w, http.StatusInternalServerError, err.Error())
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"filename": filepath.Base(abs),
			"kind":     "zip_preview",
			"entries":  entries,
		})
		return
	}

	raw, err := os.ReadFile(abs)
	if err != nil {
		writeError(w, http.StatusNotFound, "file not found")
		return
	}
	if len(raw) > 512*1024 {
		raw = raw[:512*1024]
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"filename": filepath.Base(abs),
		"kind":     "text",
		"content":  string(raw),
	})
}

type zipEntryPreview struct {
	Name    string `json:"name"`
	Size    uint64 `json:"size"`
	Content string `json:"content,omitempty"`
}

func readZipTextPreview(zipPath string) ([]zipEntryPreview, error) {
	r, err := zip.OpenReader(zipPath)
	if err != nil {
		return nil, err
	}
	defer r.Close()

	var out []zipEntryPreview
	for _, f := range r.File {
		if f.FileInfo().IsDir() {
			continue
		}
		low := strings.ToLower(f.Name)
		if strings.HasPrefix(low, "__macosx/") || strings.Contains(low, "/._") {
			continue
		}
		ep := zipEntryPreview{Name: f.Name, Size: f.UncompressedSize64}
		if (strings.HasSuffix(low, ".md") || strings.HasSuffix(low, ".txt") ||
			strings.HasSuffix(low, ".py") || strings.HasSuffix(low, ".html") ||
			strings.HasSuffix(low, ".css") || strings.HasSuffix(low, ".js")) &&
			f.UncompressedSize64 <= 200*1024 {
			if rc, err := f.Open(); err == nil {
				b, _ := io.ReadAll(io.LimitReader(rc, 200*1024))
				_ = rc.Close()
				ep.Content = string(b)
			}
		}
		out = append(out, ep)
	}
	return out, nil
}
