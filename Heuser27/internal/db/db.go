package db

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	_ "modernc.org/sqlite"
)

type Store struct {
	DB *sql.DB
}

type Student struct {
	ID               string `json:"id"`
	Name             string `json:"name"`
	Email            string `json:"email"`
	Batch            string `json:"batch"`
	EnrollmentStatus string `json:"enrollment_status"`
	Starred          bool   `json:"starred"`
	StarNote         string `json:"star_note"`
	StarredAt        string `json:"starred_at"`
	SubmissionCount  int    `json:"submission_count"`
	TotalVotes       int    `json:"total_votes"`
	TotalComments    int    `json:"total_comments"`
	PlayableCount    int    `json:"playable_count"`
	SubmittedHWs     []int  `json:"submitted_hws"`
	HasHW6Game       bool   `json:"has_hw6_game"`
	HasArcadeGame    bool   `json:"has_arcade_game"`
}

type HomeworkMeta struct {
	HWNumber        int    `json:"hw_number"`
	Title           string `json:"title"`
	Subtitle        string `json:"subtitle"`
	Kind            string `json:"kind"`
	SourceXlsx      string `json:"source_xlsx"`
	SubmissionCount int    `json:"submission_count"`
}

type Submission struct {
	ID             string `json:"id"`
	StudentID      string `json:"student_id"`
	HWNumber       int    `json:"hw_number"`
	HWTitle        string `json:"hw_title"`
	HWKind         string `json:"hw_kind"`
	SubmittedAt    string `json:"submitted_at"`
	PrimaryURL     string `json:"primary_url"`
	SecondaryURL   string `json:"secondary_url"`
	EmbedURL       string `json:"embed_url"`
	ExtraURLsJSON  string `json:"extra_urls_json"`
	LocalFilesJSON string `json:"local_files_json"`
	Feedback       string `json:"feedback"`
	RawJSON        string `json:"raw_json"`
	AttemptCount   int    `json:"attempt_count"`
	Playable       bool   `json:"playable"`
	IsLocalOnlyURL bool   `json:"is_local_only_url"`
	Votes          int    `json:"votes"`
	CommentCount   int    `json:"comment_count"`
	UserVoted      bool   `json:"user_voted"`
}

type Comment struct {
	ID           int64  `json:"id"`
	SubmissionID string `json:"submission_id"`
	StudentID    string `json:"student_id"`
	StudentName  string `json:"student_name,omitempty"`
	HWNumber     int    `json:"hw_number,omitempty"`
	AuthorName   string `json:"author_name"`
	Body         string `json:"body"`
	CommenterIP  string `json:"commenter_ip,omitempty"`
	CreatedAt    string `json:"created_at"`
}

type SyncLog struct {
	ID               int64  `json:"id"`
	Source           string `json:"source"`
	StudentsCount    int    `json:"students_count"`
	SubmissionsCount int    `json:"submissions_count"`
	Notes            string `json:"notes"`
	CreatedAt        string `json:"created_at"`
}

func Open(dbPath string) (*Store, error) {
	if err := os.MkdirAll(filepath.Dir(dbPath), 0o755); err != nil {
		return nil, fmt.Errorf("mkdir db dir: %w", err)
	}
	dsn := fmt.Sprintf("file:%s?_pragma=busy_timeout(5000)&_pragma=journal_mode(WAL)&_pragma=foreign_keys(ON)", dbPath)
	sqlDB, err := sql.Open("sqlite", dsn)
	if err != nil {
		return nil, err
	}
	sqlDB.SetMaxOpenConns(1)
	s := &Store{DB: sqlDB}
	if err := s.migrate(); err != nil {
		_ = sqlDB.Close()
		return nil, err
	}
	return s, nil
}

func (s *Store) Close() error {
	return s.DB.Close()
}

func (s *Store) migrate() error {
	schema := `
CREATE TABLE IF NOT EXISTS students (
	id TEXT PRIMARY KEY,
	name TEXT NOT NULL,
	email TEXT NOT NULL DEFAULT '',
	batch TEXT NOT NULL DEFAULT '',
	enrollment_status TEXT NOT NULL DEFAULT 'Enrolled',
	starred INTEGER NOT NULL DEFAULT 0,
	star_note TEXT NOT NULL DEFAULT '',
	starred_at TEXT NOT NULL DEFAULT '',
	updated_at TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS homeworks (
	hw_number INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	subtitle TEXT NOT NULL DEFAULT '',
	kind TEXT NOT NULL DEFAULT 'web_link',
	source_xlsx TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS submissions (
	id TEXT PRIMARY KEY,
	student_id TEXT NOT NULL,
	hw_number INTEGER NOT NULL,
	submitted_at TEXT NOT NULL DEFAULT '',
	primary_url TEXT NOT NULL DEFAULT '',
	secondary_url TEXT NOT NULL DEFAULT '',
	embed_url TEXT NOT NULL DEFAULT '',
	extra_urls_json TEXT NOT NULL DEFAULT '[]',
	local_files_json TEXT NOT NULL DEFAULT '[]',
	feedback TEXT NOT NULL DEFAULT '',
	raw_json TEXT NOT NULL DEFAULT '{}',
	attempt_count INTEGER NOT NULL DEFAULT 1,
	playable INTEGER NOT NULL DEFAULT 0,
	is_local_only_url INTEGER NOT NULL DEFAULT 0,
	FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_submissions_student ON submissions(student_id);
CREATE INDEX IF NOT EXISTS idx_submissions_hw ON submissions(hw_number);

CREATE TABLE IF NOT EXISTS votes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	submission_id TEXT NOT NULL,
	student_id TEXT NOT NULL,
	voter_ip TEXT NOT NULL,
	created_at TEXT NOT NULL DEFAULT (datetime('now')),
	UNIQUE(submission_id, voter_ip)
);

CREATE INDEX IF NOT EXISTS idx_votes_sub ON votes(submission_id);
CREATE INDEX IF NOT EXISTS idx_votes_ip ON votes(voter_ip);

CREATE TABLE IF NOT EXISTS comments (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	submission_id TEXT NOT NULL,
	student_id TEXT NOT NULL,
	author_name TEXT NOT NULL,
	body TEXT NOT NULL,
	commenter_ip TEXT NOT NULL,
	created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_comments_sub ON comments(submission_id);
CREATE INDEX IF NOT EXISTS idx_comments_student ON comments(student_id);

CREATE TABLE IF NOT EXISTS sync_logs (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	source TEXT NOT NULL,
	students_count INTEGER NOT NULL DEFAULT 0,
	submissions_count INTEGER NOT NULL DEFAULT 0,
	notes TEXT NOT NULL DEFAULT '',
	created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
`
	_, err := s.DB.Exec(schema)
	return err
}

func (s *Store) UpsertHomeworkMeta(meta HomeworkMeta) error {
	_, err := s.DB.Exec(`
		INSERT INTO homeworks (hw_number, title, subtitle, kind, source_xlsx)
		VALUES (?, ?, ?, ?, ?)
		ON CONFLICT(hw_number) DO UPDATE SET
			title = excluded.title,
			subtitle = excluded.subtitle,
			kind = excluded.kind,
			source_xlsx = excluded.source_xlsx
	`, meta.HWNumber, meta.Title, meta.Subtitle, meta.Kind, meta.SourceXlsx)
	return err
}

func (s *Store) UpsertStudent(st Student) error {
	now := time.Now().UTC().Format(time.RFC3339)
	_, err := s.DB.Exec(`
		INSERT INTO students (id, name, email, batch, enrollment_status, updated_at)
		VALUES (?, ?, ?, ?, ?, ?)
		ON CONFLICT(id) DO UPDATE SET
			name = CASE WHEN excluded.name != '' AND excluded.name NOT LIKE 'Student %' THEN excluded.name ELSE students.name END,
			email = CASE WHEN excluded.email != '' THEN excluded.email ELSE students.email END,
			batch = CASE WHEN excluded.batch != '' THEN excluded.batch ELSE students.batch END,
			enrollment_status = CASE WHEN excluded.enrollment_status != '' THEN excluded.enrollment_status ELSE students.enrollment_status END,
			updated_at = excluded.updated_at
	`, st.ID, st.Name, st.Email, st.Batch, st.EnrollmentStatus, now)
	return err
}

func (s *Store) ReplaceAllSubmissions(subs []Submission) error {
	tx, err := s.DB.Begin()
	if err != nil {
		return err
	}
	defer func() {
		if err != nil {
			_ = tx.Rollback()
		}
	}()

	if _, err = tx.Exec(`DELETE FROM submissions`); err != nil {
		return err
	}

	stmt, err := tx.Prepare(`
		INSERT INTO submissions (
			id, student_id, hw_number, submitted_at, primary_url, secondary_url, embed_url,
			extra_urls_json, local_files_json, feedback, raw_json, attempt_count, playable, is_local_only_url
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`)
	if err != nil {
		return err
	}
	defer stmt.Close()

	for _, sub := range subs {
		playable := 0
		if sub.Playable {
			playable = 1
		}
		localOnly := 0
		if sub.IsLocalOnlyURL {
			localOnly = 1
		}
		if _, err = stmt.Exec(
			sub.ID, sub.StudentID, sub.HWNumber, sub.SubmittedAt,
			sub.PrimaryURL, sub.SecondaryURL, sub.EmbedURL,
			sub.ExtraURLsJSON, sub.LocalFilesJSON, sub.Feedback, sub.RawJSON,
			sub.AttemptCount, playable, localOnly,
		); err != nil {
			return err
		}
	}

	return tx.Commit()
}

func (s *Store) LogSync(source string, studentsCount, subsCount int, notes string) error {
	_, err := s.DB.Exec(`
		INSERT INTO sync_logs (source, students_count, submissions_count, notes)
		VALUES (?, ?, ?, ?)
	`, source, studentsCount, subsCount, notes)
	return err
}

func (s *Store) ListHomeworks() ([]HomeworkMeta, error) {
	rows, err := s.DB.Query(`
		SELECT h.hw_number, h.title, h.subtitle, h.kind, h.source_xlsx,
		       COUNT(sub.id) as sub_count
		FROM homeworks h
		LEFT JOIN submissions sub ON sub.hw_number = h.hw_number
		GROUP BY h.hw_number
		ORDER BY h.hw_number ASC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []HomeworkMeta
	for rows.Next() {
		var m HomeworkMeta
		if err := rows.Scan(&m.HWNumber, &m.Title, &m.Subtitle, &m.Kind, &m.SourceXlsx, &m.SubmissionCount); err != nil {
			return nil, err
		}
		list = append(list, m)
	}
	return list, rows.Err()
}

func (s *Store) ListStudents(includeZeroSubmissions bool) ([]Student, error) {
	query := `
		SELECT st.id, st.name, st.email, st.batch, st.enrollment_status,
		       st.starred, st.star_note, st.starred_at
		FROM students st
		ORDER BY st.starred DESC, st.name ASC
	`
	rows, err := s.DB.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	studentMap := make(map[string]*Student)
	var ordered []*Student
	for rows.Next() {
		var st Student
		var starred int
		if err := rows.Scan(&st.ID, &st.Name, &st.Email, &st.Batch, &st.EnrollmentStatus,
			&starred, &st.StarNote, &st.StarredAt); err != nil {
			return nil, err
		}
		st.Starred = starred == 1
		st.SubmittedHWs = []int{}
		studentMap[st.ID] = &st
		ordered = append(ordered, &st)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}

	subRows, err := s.DB.Query(`
		SELECT sub.id, sub.student_id, sub.hw_number, sub.playable, sub.embed_url,
		       (SELECT COUNT(*) FROM votes v WHERE v.submission_id = sub.id) AS vote_cnt,
		       (SELECT COUNT(*) FROM comments c WHERE c.submission_id = sub.id) AS cmt_cnt
		FROM submissions sub
		ORDER BY sub.hw_number ASC
	`)
	if err != nil {
		return nil, err
	}
	defer subRows.Close()

	for subRows.Next() {
		var subID, studentID, embedURL string
		var hwNum, playable, vCnt, cCnt int
		if err := subRows.Scan(&subID, &studentID, &hwNum, &playable, &embedURL, &vCnt, &cCnt); err != nil {
			return nil, err
		}
		st, ok := studentMap[studentID]
		if !ok {
			continue
		}
		st.SubmissionCount++
		st.SubmittedHWs = append(st.SubmittedHWs, hwNum)
		st.TotalVotes += vCnt
		st.TotalComments += cCnt
		if playable == 1 {
			st.PlayableCount++
		}
		if hwNum == 6 && strings.HasPrefix(embedURL, "/play/hw6/") {
			st.HasHW6Game = true
		}
		if (hwNum == 1 || hwNum == 2) && embedURL != "" {
			st.HasArcadeGame = true
		}
	}
	if err := subRows.Err(); err != nil {
		return nil, err
	}

	var result []Student
	for _, st := range ordered {
		if !includeZeroSubmissions && st.SubmissionCount == 0 && !st.Starred {
			continue
		}
		result = append(result, *st)
	}
	return result, nil
}

func (s *Store) GetStudent(studentID string, viewerIP string) (*Student, []Submission, error) {
	var st Student
	var starred int
	err := s.DB.QueryRow(`
		SELECT id, name, email, batch, enrollment_status, starred, star_note, starred_at
		FROM students WHERE id = ?
	`, studentID).Scan(&st.ID, &st.Name, &st.Email, &st.Batch, &st.EnrollmentStatus,
		&starred, &st.StarNote, &st.StarredAt)
	if err != nil {
		return nil, nil, err
	}
	st.Starred = starred == 1
	st.SubmittedHWs = []int{}

	rows, err := s.DB.Query(`
		SELECT sub.id, sub.student_id, sub.hw_number,
		       COALESCE(h.title, 'Homework ' || sub.hw_number),
		       COALESCE(h.kind, 'web_link'),
		       sub.submitted_at, sub.primary_url, sub.secondary_url, sub.embed_url,
		       sub.extra_urls_json, sub.local_files_json, sub.feedback, sub.raw_json,
		       sub.attempt_count, sub.playable, sub.is_local_only_url,
		       (SELECT COUNT(*) FROM votes v WHERE v.submission_id = sub.id) AS vote_cnt,
		       (SELECT COUNT(*) FROM comments c WHERE c.submission_id = sub.id) AS cmt_cnt,
		       EXISTS(SELECT 1 FROM votes v2 WHERE v2.submission_id = sub.id AND v2.voter_ip = ?) AS user_voted
		FROM submissions sub
		LEFT JOIN homeworks h ON h.hw_number = sub.hw_number
		WHERE sub.student_id = ?
		ORDER BY sub.hw_number ASC
	`, viewerIP, studentID)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var subs []Submission
	for rows.Next() {
		var sub Submission
		var playable, localOnly, userVoted int
		if err := rows.Scan(
			&sub.ID, &sub.StudentID, &sub.HWNumber, &sub.HWTitle, &sub.HWKind,
			&sub.SubmittedAt, &sub.PrimaryURL, &sub.SecondaryURL, &sub.EmbedURL,
			&sub.ExtraURLsJSON, &sub.LocalFilesJSON, &sub.Feedback, &sub.RawJSON,
			&sub.AttemptCount, &playable, &localOnly,
			&sub.Votes, &sub.CommentCount, &userVoted,
		); err != nil {
			return nil, nil, err
		}
		sub.Playable = playable == 1
		sub.IsLocalOnlyURL = localOnly == 1
		sub.UserVoted = userVoted == 1
		st.SubmissionCount++
		st.SubmittedHWs = append(st.SubmittedHWs, sub.HWNumber)
		st.TotalVotes += sub.Votes
		st.TotalComments += sub.CommentCount
		if sub.Playable {
			st.PlayableCount++
		}
		if sub.HWNumber == 6 && strings.HasPrefix(sub.EmbedURL, "/play/hw6/") {
			st.HasHW6Game = true
		}
		if (sub.HWNumber == 1 || sub.HWNumber == 2) && sub.EmbedURL != "" {
			st.HasArcadeGame = true
		}
		subs = append(subs, sub)
	}
	return &st, subs, rows.Err()
}

func (s *Store) ToggleVote(submissionID, voterIP string) (voted bool, total int, err error) {
	var studentID string
	err = s.DB.QueryRow(`SELECT student_id FROM submissions WHERE id = ?`, submissionID).Scan(&studentID)
	if err != nil {
		return false, 0, err
	}

	var exists int
	err = s.DB.QueryRow(`SELECT COUNT(*) FROM votes WHERE submission_id = ? AND voter_ip = ?`, submissionID, voterIP).Scan(&exists)
	if err != nil {
		return false, 0, err
	}

	if exists > 0 {
		if _, err := s.DB.Exec(`DELETE FROM votes WHERE submission_id = ? AND voter_ip = ?`, submissionID, voterIP); err != nil {
			return false, 0, err
		}
		voted = false
	} else {
		if _, err := s.DB.Exec(`INSERT INTO votes (submission_id, student_id, voter_ip) VALUES (?, ?, ?)`, submissionID, studentID, voterIP); err != nil {
			return false, 0, err
		}
		voted = true
	}

	err = s.DB.QueryRow(`SELECT COUNT(*) FROM votes WHERE submission_id = ?`, submissionID).Scan(&total)
	return voted, total, err
}

func (s *Store) ListComments(studentID, submissionID string, includeIP bool) ([]Comment, error) {
	var rows *sql.Rows
	var err error
	if submissionID != "" {
		rows, err = s.DB.Query(`
			SELECT c.id, c.submission_id, c.student_id, COALESCE(st.name,''), COALESCE(sub.hw_number,0),
			       c.author_name, c.body, c.commenter_ip, c.created_at
			FROM comments c
			LEFT JOIN students st ON st.id = c.student_id
			LEFT JOIN submissions sub ON sub.id = c.submission_id
			WHERE c.submission_id = ?
			ORDER BY c.id DESC
		`, submissionID)
	} else if studentID != "" {
		rows, err = s.DB.Query(`
			SELECT c.id, c.submission_id, c.student_id, COALESCE(st.name,''), COALESCE(sub.hw_number,0),
			       c.author_name, c.body, c.commenter_ip, c.created_at
			FROM comments c
			LEFT JOIN students st ON st.id = c.student_id
			LEFT JOIN submissions sub ON sub.id = c.submission_id
			WHERE c.student_id = ?
			ORDER BY c.id DESC
		`, studentID)
	} else {
		rows, err = s.DB.Query(`
			SELECT c.id, c.submission_id, c.student_id, COALESCE(st.name,''), COALESCE(sub.hw_number,0),
			       c.author_name, c.body, c.commenter_ip, c.created_at
			FROM comments c
			LEFT JOIN students st ON st.id = c.student_id
			LEFT JOIN submissions sub ON sub.id = c.submission_id
			ORDER BY c.id DESC
			LIMIT 200
		`)
	}
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var list []Comment
	for rows.Next() {
		var c Comment
		var ip string
		if err := rows.Scan(&c.ID, &c.SubmissionID, &c.StudentID, &c.StudentName, &c.HWNumber, &c.AuthorName, &c.Body, &ip, &c.CreatedAt); err != nil {
			return nil, err
		}
		if includeIP {
			c.CommenterIP = ip
		}
		list = append(list, c)
	}
	return list, rows.Err()
}

func (s *Store) AddComment(submissionID, authorName, body, commenterIP string) (*Comment, error) {
	var studentID string
	if err := s.DB.QueryRow(`SELECT student_id FROM submissions WHERE id = ?`, submissionID).Scan(&studentID); err != nil {
		return nil, err
	}

	// Rate limit: max 8 comments in last 5 minutes per IP
	var recentCount int
	_ = s.DB.QueryRow(`
		SELECT COUNT(*) FROM comments
		WHERE commenter_ip = ? AND created_at >= datetime('now', '-5 minutes')
	`, commenterIP).Scan(&recentCount)
	if recentCount >= 8 {
		return nil, fmt.Errorf("rate limit exceeded: please wait a moment before posting more comments")
	}

	res, err := s.DB.Exec(`
		INSERT INTO comments (submission_id, student_id, author_name, body, commenter_ip)
		VALUES (?, ?, ?, ?, ?)
	`, submissionID, studentID, authorName, body, commenterIP)
	if err != nil {
		return nil, err
	}
	id, _ := res.LastInsertId()

	var c Comment
	err = s.DB.QueryRow(`
		SELECT id, submission_id, student_id, author_name, body, created_at
		FROM comments WHERE id = ?
	`, id).Scan(&c.ID, &c.SubmissionID, &c.StudentID, &c.AuthorName, &c.Body, &c.CreatedAt)
	return &c, err
}

func (s *Store) DeleteComment(commentID int64) error {
	_, err := s.DB.Exec(`DELETE FROM comments WHERE id = ?`, commentID)
	return err
}

func (s *Store) SetStudentStar(studentID string, starred bool, note string) error {
	val := 0
	ts := ""
	if starred {
		val = 1
		ts = time.Now().UTC().Format(time.RFC3339)
	}
	_, err := s.DB.Exec(`
		UPDATE students SET starred = ?, star_note = ?, starred_at = ?
		WHERE id = ?
	`, val, note, ts, studentID)
	return err
}

func (s *Store) RecentSyncLogs() ([]SyncLog, error) {
	rows, err := s.DB.Query(`
		SELECT id, source, students_count, submissions_count, notes, created_at
		FROM sync_logs ORDER BY id DESC LIMIT 15
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []SyncLog
	for rows.Next() {
		var l SyncLog
		if err := rows.Scan(&l.ID, &l.Source, &l.StudentsCount, &l.SubmissionsCount, &l.Notes, &l.CreatedAt); err != nil {
			return nil, err
		}
		out = append(out, l)
	}
	return out, rows.Err()
}
