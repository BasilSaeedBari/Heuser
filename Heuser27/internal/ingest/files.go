package ingest

import (
	"archive/zip"
	"io"
	"os"
	"path/filepath"
	"strings"
)

type localFileEntry struct {
	Label   string
	RelPath string
	AbsPath string
	NameLow string
	Kind    string
	IsPlan  bool
}

func indexHomeworkFiles(baseDir, hwDir string) []localFileEntry {
	var out []localFileEntry
	_ = filepath.WalkDir(hwDir, func(path string, d os.DirEntry, err error) error {
		if err != nil || d.IsDir() {
			return nil
		}
		// Only index files inside "(File responses)" subdirectories, not root .tex/.pdf/.xlsx
		if path == hwDir || filepath.Dir(path) == hwDir {
			return nil
		}
		name := d.Name()
		low := strings.ToLower(name)
		rel, err := filepath.Rel(baseDir, path)
		if err != nil {
			return nil
		}
		relSlash := filepath.ToSlash(rel)

		kind := classifyFileKind(low)
		label := filepath.Base(filepath.Dir(path))
		label = strings.TrimSpace(strings.TrimSuffix(label, "(File responses)"))
		isPlan := strings.Contains(strings.ToLower(relSlash), "plans") || strings.Contains(low, "plan")

		out = append(out, localFileEntry{
			Label:   label + " — " + name,
			RelPath: relSlash,
			AbsPath: path,
			NameLow: low,
			Kind:    kind,
			IsPlan:  isPlan,
		})
		return nil
	})
	return out
}

func classifyFileKind(low string) string {
	switch {
	case strings.Contains(low, ".py"):
		return "python"
	case strings.HasSuffix(low, ".md"):
		return "markdown"
	case strings.HasSuffix(low, ".html") || strings.HasSuffix(low, ".htm"):
		return "html"
	case strings.HasSuffix(low, ".zip"):
		return "zip"
	case strings.HasSuffix(low, ".rar"):
		return "archive"
	default:
		return "text"
	}
}

func matchLocalFiles(index []localFileEntry, sid, studentName string) []localFileEntry {
	var matched []localFileEntry
	seen := make(map[string]bool)

	for _, f := range index {
		if sid != "" && strings.Contains(f.NameLow, strings.ToLower(sid)) {
			matched = append(matched, f)
			seen[f.RelPath] = true
		}
	}

	// Secondary match for rare files missing ID in filename (e.g. "KUMAIL MOHAMMAD ROKER")
	if len(matched) == 0 && studentName != "" {
		tokens := strings.Fields(strings.ToLower(studentName))
		for _, f := range index {
			if seen[f.RelPath] {
				continue
			}
			hits := 0
			for _, t := range tokens {
				if len(t) >= 4 && strings.Contains(f.NameLow, t) {
					hits++
				}
			}
			if hits >= 2 || (len(tokens) == 1 && hits == 1) {
				matched = append(matched, f)
				seen[f.RelPath] = true
			}
		}
	}

	return matched
}

func prepareHW6Game(baseDir, dataDir, sid string, files []localFileEntry) bool {
	targetDir := filepath.Join(dataDir, "hw6_games", sid)
	_ = os.RemoveAll(targetDir)

	// Prefer Code Files zip, then any non-plan zip, then standalone html/txt
	var candidates []localFileEntry
	for _, f := range files {
		if f.Kind == "zip" && strings.Contains(strings.ToLower(f.RelPath), "code files") && !strings.Contains(f.NameLow, "_plan") {
			candidates = append(candidates, f)
		}
	}
	for _, f := range files {
		if f.Kind == "zip" && !f.IsPlan {
			candidates = append(candidates, f)
		}
	}

	for _, c := range candidates {
		if extractWebGameZip(c.AbsPath, targetDir) {
			return true
		}
		_ = os.RemoveAll(targetDir)
	}

	// Fallback: standalone HTML or !DOCTYPE html .txt file in Code Files
	for _, f := range files {
		if !strings.Contains(strings.ToLower(f.RelPath), "code files") {
			continue
		}
		if f.Kind == "html" || strings.Contains(f.NameLow, "doctype html") {
			raw, err := os.ReadFile(f.AbsPath)
			if err != nil {
				continue
			}
			lowBody := strings.ToLower(string(raw))
			if strings.Contains(lowBody, "<html") || strings.Contains(lowBody, "<!doctype") {
				if err := os.MkdirAll(targetDir, 0o755); err != nil {
					return false
				}
				if err := os.WriteFile(filepath.Join(targetDir, "index.html"), raw, 0o644); err == nil {
					return true
				}
			}
		}
	}

	return false
}

func extractWebGameZip(zipPath, targetDir string) bool {
	r, err := zip.OpenReader(zipPath)
	if err != nil {
		return false
	}
	defer r.Close()

	if err := os.MkdirAll(targetDir, 0o755); err != nil {
		return false
	}

	// Collect non-junk entries to detect if all files sit inside one top-level folder
	var validFiles []*zip.File
	for _, f := range r.File {
		if f.FileInfo().IsDir() {
			continue
		}
		clean := filepath.ToSlash(filepath.Clean(f.Name))
		if strings.HasPrefix(clean, "__MACOSX/") || strings.Contains(clean, "/._") || strings.HasPrefix(filepath.Base(clean), "._") {
			continue
		}
		if strings.HasPrefix(clean, "..") || strings.HasPrefix(clean, "/") {
			continue
		}
		validFiles = append(validFiles, f)
	}
	if len(validFiles) == 0 {
		return false
	}

	// Detect common top-level directory prefix
	commonPrefix := ""
	firstParts := strings.Split(filepath.ToSlash(filepath.Clean(validFiles[0].Name)), "/")
	if len(firstParts) > 1 {
		candidate := firstParts[0] + "/"
		allShare := true
		for _, f := range validFiles {
			if !strings.HasPrefix(filepath.ToSlash(filepath.Clean(f.Name)), candidate) {
				allShare = false
				break
			}
		}
		if allShare {
			commonPrefix = candidate
		}
	}

	hasIndex := false
	var firstHTML string

	for _, f := range validFiles {
		rel := filepath.ToSlash(filepath.Clean(f.Name))
		if commonPrefix != "" {
			rel = strings.TrimPrefix(rel, commonPrefix)
		}
		if rel == "" || strings.HasPrefix(rel, "..") {
			continue
		}

		// Handle students who accidentally submitted index.html.txt / style.css.txt / script.js.txt
		lowRel := strings.ToLower(rel)
		if strings.HasSuffix(lowRel, ".html.txt") || strings.HasSuffix(lowRel, ".css.txt") || strings.HasSuffix(lowRel, ".js.txt") {
			rel = rel[:len(rel)-4]
			lowRel = strings.ToLower(rel)
		}

		destPath := filepath.Join(targetDir, filepath.FromSlash(rel))
		if !strings.HasPrefix(filepath.Clean(destPath), filepath.Clean(targetDir)) {
			continue
		}
		if err := os.MkdirAll(filepath.Dir(destPath), 0o755); err != nil {
			continue
		}

		rc, err := f.Open()
		if err != nil {
			continue
		}
		out, err := os.Create(destPath)
		if err != nil {
			_ = rc.Close()
			continue
		}
		_, copyErr := io.CopyN(out, rc, 10*1024*1024) // 10MB per file safety cap
		_ = out.Close()
		_ = rc.Close()
		if copyErr != nil && copyErr != io.EOF {
			continue
		}

		if lowRel == "index.html" {
			hasIndex = true
		} else if firstHTML == "" && strings.HasSuffix(lowRel, ".html") {
			firstHTML = destPath
		}
	}

	if !hasIndex && firstHTML != "" {
		// Copy firstHTML to index.html if it sits at root or copy its content
		if raw, err := os.ReadFile(firstHTML); err == nil {
			_ = os.WriteFile(filepath.Join(targetDir, "index.html"), raw, 0o644)
			hasIndex = true
		}
	}

	if !hasIndex {
		return false
	}

	// Verify index.html isn't an empty stub (e.g. < 30 bytes)
	info, err := os.Stat(filepath.Join(targetDir, "index.html"))
	if err != nil || info.Size() < 30 {
		return false
	}

	return true
}
