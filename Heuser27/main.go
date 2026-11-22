package main

import (
	"context"
	"embed"
	"log"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"

	"heuser27/internal/db"
	"heuser27/internal/ingest"
	"heuser27/internal/server"
)

//go:embed all:web
var webFS embed.FS

func main() {
	port := envOr("PORT", "8090")
	baseDir := envOr("BASE_DIR", ".")
	dataDir := envOr("DATA_DIR", filepath.Join(baseDir, "data"))
	adminPass := envOr("ADMIN_PASSWORD", "heuser27admin")

	absBase, err := filepath.Abs(baseDir)
	if err != nil {
		log.Fatalf("resolve base dir: %v", err)
	}
	absData, err := filepath.Abs(dataDir)
	if err != nil {
		log.Fatalf("resolve data dir: %v", err)
	}

	dbPath := filepath.Join(absData, "heuser27.db")
	store, err := db.Open(dbPath)
	if err != nil {
		log.Fatalf("open sqlite db: %v", err)
	}
	defer store.Close()

	log.Printf("Syncing homework submissions from %s ...", absBase)
	res, err := ingest.SyncAll(store, absBase, absData, "startup")
	if err != nil {
		log.Fatalf("initial ingest failed: %v", err)
	}
	log.Printf("Sync complete: %d students, %d submissions, %d homeworks, %d playable HW6 web games",
		res.StudentsCount, res.SubmissionsCount, res.HomeworksCount, res.HW6PlayableCount)

	srv := server.New(store, absBase, absData, adminPass, webFS)
	httpSrv := &http.Server{
		Addr:              ":" + port,
		Handler:           srv.Handler(),
		ReadHeaderTimeout: 10 * time.Second,
		WriteTimeout:      60 * time.Second,
		IdleTimeout:       120 * time.Second,
	}

	go func() {
		log.Printf("Heuser27 CRP Showcase listening on http://localhost:%s", port)
		if err := httpSrv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("http server error: %v", err)
		}
	}()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
	<-stop
	log.Println("Shutting down...")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	_ = httpSrv.Shutdown(ctx)
}

func envOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
