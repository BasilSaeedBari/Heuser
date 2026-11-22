package server

import (
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"embed"
	"encoding/hex"
	"encoding/json"
	"io/fs"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"

	"heuser27/internal/db"
)

type Server struct {
	Store         *db.Store
	BaseDir       string
	DataDir       string
	AdminPassword string
	SessionSecret []byte
	WebFS         embed.FS
	SyncMu        sync.Mutex
}

func New(store *db.Store, baseDir, dataDir, adminPass string, webFS embed.FS) *Server {
	secret := make([]byte, 32)
	if envSec := os.Getenv("SESSION_SECRET"); envSec != "" {
		sum := sha256.Sum256([]byte(envSec))
		secret = sum[:]
	} else {
		_, _ = rand.Read(secret)
	}
	if adminPass == "" {
		adminPass = "heuser27admin"
	}
	return &Server{
		Store:         store,
		BaseDir:       baseDir,
		DataDir:       dataDir,
		AdminPassword: adminPass,
		SessionSecret: secret,
		WebFS:         webFS,
	}
}

func (s *Server) Handler() http.Handler {
	mux := http.NewServeMux()

	// Embedded static assets
	subWeb, _ := fs.Sub(s.WebFS, "web")
	assetsSub, _ := fs.Sub(subWeb, "assets")
	mux.Handle("GET /assets/", http.StripPrefix("/assets/", http.FileServer(http.FS(assetsSub))))

	// Page routes
	mux.HandleFunc("GET /{$}", s.servePage("web/index.html"))
	mux.HandleFunc("GET /student/{id}", s.servePage("web/student.html"))
	mux.HandleFunc("GET /student", s.servePage("web/student.html"))
	mux.HandleFunc("GET /admin", s.servePage("web/admin.html"))
	mux.HandleFunc("GET /admin/", s.servePage("web/admin.html"))
	mux.HandleFunc("GET /healthz", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
	})

	// Sandboxed HW6 game runner
	mux.HandleFunc("GET /play/hw6/", s.handlePlayHW6)

	// Safe local submission file viewer (.py, .md, .txt)
	mux.HandleFunc("GET /api/file", s.handleGetLocalFile)

	// Public Showcase & Interactive APIs
	mux.HandleFunc("GET /api/showcase", s.handleShowcase)
	mux.HandleFunc("GET /api/student/{id}", s.handleGetStudent)
	mux.HandleFunc("POST /api/vote", s.handleToggleVote)
	mux.HandleFunc("POST /api/comments", s.handleAddComment)

	// Admin APIs
	mux.HandleFunc("GET /api/admin/me", s.handleAdminMe)
	mux.HandleFunc("POST /api/admin/login", s.handleAdminLogin)
	mux.HandleFunc("POST /api/admin/logout", s.handleAdminLogout)
	mux.HandleFunc("GET /api/admin/summary", s.requireAdmin(s.handleAdminSummary))
	mux.HandleFunc("POST /api/admin/star", s.requireAdmin(s.handleAdminStar))
	mux.HandleFunc("POST /api/admin/resync", s.requireAdmin(s.handleAdminResync))
	mux.HandleFunc("POST /api/admin/upload-xlsx", s.requireAdmin(s.handleAdminUploadXlsx))
	mux.HandleFunc("DELETE /api/admin/comments/{id}", s.requireAdmin(s.handleAdminDeleteComment))
	mux.HandleFunc("GET /api/admin/export.csv", s.requireAdmin(s.handleAdminExportCSV))

	return withSecurityHeaders(mux)
}

func (s *Server) servePage(path string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		data, err := s.WebFS.ReadFile(path)
		if err != nil {
			http.NotFound(w, r)
			return
		}
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		_, _ = w.Write(data)
	}
}

func (s *Server) handlePlayHW6(w http.ResponseWriter, r *http.Request) {
	// URL format: /play/hw6/<student_id>/<subpath>
	trimmed := strings.TrimPrefix(r.URL.Path, "/play/hw6/")
	parts := strings.SplitN(trimmed, "/", 2)
	if len(parts) == 0 || parts[0] == "" {
		http.NotFound(w, r)
		return
	}
	sid := filepath.Base(parts[0])
	if sid == "." || sid == ".." || strings.ContainsAny(sid, `/\`) {
		http.NotFound(w, r)
		return
	}
	relPath := "index.html"
	if len(parts) == 2 && parts[1] != "" {
		relPath = parts[1]
	}

	gameRoot := filepath.Join(s.DataDir, "hw6_games", sid)
	target := filepath.Join(gameRoot, filepath.FromSlash(filepath.Clean("/"+relPath)))
	if !strings.HasPrefix(filepath.Clean(target), filepath.Clean(gameRoot)) {
		http.Error(w, "forbidden", http.StatusForbidden)
		return
	}

	if info, err := os.Stat(target); err == nil && info.IsDir() {
		target = filepath.Join(target, "index.html")
	}
	if _, err := os.Stat(target); err != nil {
		http.NotFound(w, r)
		return
	}

	// Sandbox student-submitted HTML/JS so it cannot access parent cookies or origin storage maliciously
	w.Header().Set("X-Frame-Options", "SAMEORIGIN")
	w.Header().Set("Content-Security-Policy", "sandbox allow-scripts allow-pointer-lock allow-modals; default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:;")
	http.ServeFile(w, r, target)
}

func withSecurityHeaders(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("Referrer-Policy", "strict-origin-when-cross-origin")
		next.ServeHTTP(w, r)
	})
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func writeError(w http.ResponseWriter, status int, msg string) {
	writeJSON(w, status, map[string]string{"error": msg})
}

func clientIP(r *http.Request) string {
	if xff := r.Header.Get("X-Forwarded-For"); xff != "" {
		parts := strings.Split(xff, ",")
		if len(parts) > 0 {
			ip := strings.TrimSpace(parts[0])
			if ip != "" {
				return ip
			}
		}
	}
	if xri := strings.TrimSpace(r.Header.Get("X-Real-Ip")); xri != "" {
		return xri
	}
	host, _, err := net.SplitHostPort(r.RemoteAddr)
	if err == nil && host != "" {
		return host
	}
	return r.RemoteAddr
}

func (s *Server) signAdminToken() string {
	mac := hmac.New(sha256.New, s.SessionSecret)
	mac.Write([]byte("heuser27-admin-session-v1"))
	return hex.EncodeToString(mac.Sum(nil))
}

func (s *Server) isAdmin(r *http.Request) bool {
	c, err := r.Cookie("heuser27_admin")
	if err != nil {
		return false
	}
	expected := s.signAdminToken()
	return hmac.Equal([]byte(c.Value), []byte(expected))
}

func (s *Server) requireAdmin(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if !s.isAdmin(r) {
			writeError(w, http.StatusUnauthorized, "admin authentication required")
			return
		}
		next(w, r)
	}
}
