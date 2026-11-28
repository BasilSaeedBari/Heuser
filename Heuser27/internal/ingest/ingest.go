package ingest

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/xuri/excelize/v2"
	"heuser27/internal/db"
)

type RosterSeedEntry struct {
	ID     string `json:"id"`
	Name   string `json:"name"`
	Email  string `json:"email"`
	Batch  string `json:"batch"`
	Status string `json:"status"`
}

type LabeledURL struct {
	Label string `json:"label"`
	URL   string `json:"url"`
}

type LocalFileRef struct {
	Label   string `json:"label"`
	RelPath string `json:"rel_path"`
	Kind    string `json:"kind"` // python, markdown, html, zip, text
}

type HomeworkDefinition struct {
	Title    string
	Subtitle string
	Kind     string
}

var defaultHWDefs = map[int]HomeworkDefinition{
	1: {
		Title:    "Homework 1: MakeCode Arcade Intro",
		Subtitle: "First interactive block-coded arcade game",
		Kind:     "makecode",
	},
	2: {
		Title:    "Homework 2: Narrative Micro-Game",
		Subtitle: "Story-driven MakeCode Arcade game with dialogue & choices",
		Kind:     "makecode",
	},
	3: {
		Title:    "Homework 3: Problem Solving Lab",
		Subtitle: "Foundational logic & computational thinking",
		Kind:     "general",
	},
	4: {
		Title:    "Homework 4: Python Functions & Waves",
		Subtitle: "Animated Wave & Women in STEM Python programs",
		Kind:     "python",
	},
	5: {
		Title:    "Homework 5: Context & Prompt Engineering",
		Subtitle: "Research Paper Library & Knowledge Graph built with AI",
		Kind:     "ai_app",
	},
	6: {
		Title:    "Homework 6: AI Agents Web Game",
		Subtitle: "5-stage Architect & Builder interactive browser game",
		Kind:     "web_game",
	},
	7: {
		Title:    "Homework 7: First GitHub Pages Site",
		Subtitle: "Hosting Homework 6 live on GitHub Pages",
		Kind:     "web_link",
	},
	8: {
		Title:    "Homework 8: Unconventional Portfolio",
		Subtitle: "Personal creative portfolio with non-traditional navigation",
		Kind:     "web_link",
	},
	9: {
		Title:    "Homework 9: Backend Web Server",
		Subtitle: "Full-stack Python backend deployed to Render / PythonAnywhere / Vercel",
		Kind:     "backend_app",
	},
	10: {
		Title:    "Homework 10: Embedded ESP32 in Wokwi",
		Subtitle: "Single-technology Wokwi hardware simulation linked to backend server",
		Kind:     "embedded",
	},
}

var (
	reHWDir        = regexp.MustCompile(`(?i)^homework\s*(\d+)$`)
	reFullID       = regexp.MustCompile(`202801\d{4}`)
	reAnyURL       = regexp.MustCompile(`https?://[^\s<>"'\)]+`)
	reMakeCodeID   = regexp.MustCompile(`https?://(?:arcade\.)?makecode\.com/(S\d{5}-\d{5}-\d{5}-\d{5}|_[A-Za-z0-9]+|\d{5}-\d{5}-\d{5}-\d{5})`)
	reDriveID      = regexp.MustCompile(`[?&]id=([A-Za-z0-9_-]+)`)
	reMultiWS      = regexp.MustCompile(`\s+`)
)

type SyncResult struct {
	StudentsCount    int `json:"students_count"`
	SubmissionsCount int `json:"submissions_count"`
	HomeworksCount   int `json:"homeworks_count"`
	HW6PlayableCount int `json:"hw6_playable_count"`
}

func SyncAll(store *db.Store, baseDir, dataDir, sourceLabel string) (*SyncResult, error) {
	seedPath := filepath.Join(baseDir, "seed", "roster_seed.json")
	if _, statErr := os.Stat(seedPath); os.IsNotExist(statErr) {
		seedPath = filepath.Join(baseDir, "data", "roster_seed.json")
	}
	rosterByID, rosterList, err := loadRosterSeed(seedPath)
	if err != nil {
		return nil, err
	}

	// Upsert seeded students first so enrolled students with 0 submissions still appear in Admin Summary
	studentsMap := make(map[string]db.Student)
	for _, r := range rosterList {
		if r.ID == "" {
			continue
		}
		st := db.Student{
			ID:               r.ID,
			Name:             cleanName(r.Name),
			Email:            strings.TrimSpace(r.Email),
			Batch:            strings.TrimSpace(r.Batch),
			EnrollmentStatus: strings.TrimSpace(r.Status),
		}
		if st.EnrollmentStatus == "" {
			st.EnrollmentStatus = "Enrolled"
		}
		studentsMap[st.ID] = st
	}

	hwDirs, err := discoverHomeworkDirs(baseDir, dataDir)
	if err != nil {
		return nil, err
	}

	var allSubs []db.Submission
	hw6PlayableCount := 0

	for _, hw := range hwDirs {
		def := getHWDef(hw.Number)
		if err := store.UpsertHomeworkMeta(db.HomeworkMeta{
			HWNumber:   hw.Number,
			Title:      def.Title,
			Subtitle:   def.Subtitle,
			Kind:       def.Kind,
			SourceXlsx: hw.XlsxRelPath,
		}); err != nil {
			return nil, err
		}

		// Index local files in this homework folder
		localIndex := indexHomeworkFiles(baseDir, hw.DirPath)

		if hw.XlsxPath == "" {
			continue
		}

		subs, err := parseHomeworkXlsx(hw, def, baseDir, dataDir, rosterByID, rosterList, studentsMap, localIndex)
		if err != nil {
			return nil, fmt.Errorf("parse HW%d (%s): %w", hw.Number, hw.XlsxPath, err)
		}
		for _, sub := range subs {
			if sub.HWNumber == 6 && strings.HasPrefix(sub.EmbedURL, "/play/hw6/") {
				hw6PlayableCount++
			}
			allSubs = append(allSubs, sub)
		}
	}

	// Upsert all students discovered or seeded
	for _, st := range studentsMap {
		if err := store.UpsertStudent(st); err != nil {
			return nil, fmt.Errorf("upsert student %s: %w", st.ID, err)
		}
	}

	if err := store.ReplaceAllSubmissions(allSubs); err != nil {
		return nil, fmt.Errorf("replace submissions: %w", err)
	}

	notes := fmt.Sprintf("Synced %d homeworks, %d students, %d submissions (%d HW6 playable games)",
		len(hwDirs), len(studentsMap), len(allSubs), hw6PlayableCount)
	_ = store.LogSync(sourceLabel, len(studentsMap), len(allSubs), notes)

	return &SyncResult{
		StudentsCount:    len(studentsMap),
		SubmissionsCount: len(allSubs),
		HomeworksCount:   len(hwDirs),
		HW6PlayableCount: hw6PlayableCount,
	}, nil
}

type hwDirInfo struct {
	Number      int
	DirPath     string
	XlsxPath    string
	XlsxRelPath string
}

func discoverHomeworkDirs(baseDir, dataDir string) ([]hwDirInfo, error) {
	entries, err := os.ReadDir(baseDir)
	if err != nil {
		return nil, err
	}

	byNum := make(map[int]hwDirInfo)
	for _, e := range entries {
		if !e.IsDir() {
			continue
		}
		m := reHWDir.FindStringSubmatch(e.Name())
		if m == nil {
			continue
		}
		num, err := strconv.Atoi(m[1])
		if err != nil {
			continue
		}
		dirPath := filepath.Join(baseDir, e.Name())
		xlsxPath := findNewestXlsx(dirPath)
		rel := ""
		if xlsxPath != "" {
			rel, _ = filepath.Rel(baseDir, xlsxPath)
			rel = filepath.ToSlash(rel)
		}
		byNum[num] = hwDirInfo{
			Number:      num,
			DirPath:     dirPath,
			XlsxPath:    xlsxPath,
			XlsxRelPath: rel,
		}
	}

	// Check uploaded overrides in <dataDir>/uploads/hw<N>/
	uploadsRoot := filepath.Join(dataDir, "uploads")
	if upEntries, err := os.ReadDir(uploadsRoot); err == nil {
		for _, e := range upEntries {
			if !e.IsDir() || !strings.HasPrefix(strings.ToLower(e.Name()), "hw") {
				continue
			}
			numStr := strings.TrimPrefix(strings.ToLower(e.Name()), "hw")
			num, err := strconv.Atoi(numStr)
			if err != nil {
				continue
			}
			upXlsx := findNewestXlsx(filepath.Join(uploadsRoot, e.Name()))
			if upXlsx == "" {
				continue
			}
			info := byNum[num]
			info.Number = num
			info.XlsxPath = upXlsx
			info.XlsxRelPath = "uploaded:" + filepath.Base(upXlsx)
			byNum[num] = info
		}
	}

	var nums []int
	for n := range byNum {
		nums = append(nums, n)
	}
	sort.Ints(nums)

	var out []hwDirInfo
	for _, n := range nums {
		out = append(out, byNum[n])
	}
	return out, nil
}

func findNewestXlsx(dir string) string {
	entries, err := os.ReadDir(dir)
	if err != nil {
		return ""
	}
	var best string
	var bestMod time.Time
	for _, e := range entries {
		if e.IsDir() || !strings.HasSuffix(strings.ToLower(e.Name()), ".xlsx") {
			continue
		}
		if strings.HasPrefix(e.Name(), "~$") {
			continue
		}
		info, err := e.Info()
		if err != nil {
			continue
		}
		if best == "" || info.ModTime().After(bestMod) {
			best = filepath.Join(dir, e.Name())
			bestMod = info.ModTime()
		}
	}
	return best
}

func getHWDef(num int) HomeworkDefinition {
	if d, ok := defaultHWDefs[num]; ok {
		return d
	}
	return HomeworkDefinition{
		Title:    fmt.Sprintf("Homework %d", num),
		Subtitle: "Student submissions",
		Kind:     "web_link",
	}
}

func loadRosterSeed(path string) (map[string]RosterSeedEntry, []RosterSeedEntry, error) {
	byID := make(map[string]RosterSeedEntry)
	raw, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return byID, nil, nil
		}
		return nil, nil, err
	}
	// Strip UTF-8 BOM if present (PowerShell ConvertTo-Json/Out-File writes BOM in PS 5.1)
	raw = []byte(strings.TrimPrefix(string(raw), "\xef\xbb\xbf"))
	var list []RosterSeedEntry
	if err := json.Unmarshal(raw, &list); err != nil {
		return nil, nil, fmt.Errorf("parse roster_seed.json: %w", err)
	}
	for _, e := range list {
		if e.ID != "" {
			byID[e.ID] = e
		}
	}
	return byID, list, nil
}

func parseHomeworkXlsx(
	hw hwDirInfo,
	def HomeworkDefinition,
	baseDir, dataDir string,
	rosterByID map[string]RosterSeedEntry,
	rosterList []RosterSeedEntry,
	studentsMap map[string]db.Student,
	localIndex []localFileEntry,
) ([]db.Submission, error) {
	f, err := excelize.OpenFile(hw.XlsxPath)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	sheets := f.GetSheetList()
	if len(sheets) == 0 {
		return nil, nil
	}
	rows, err := f.GetRows(sheets[0])
	if err != nil {
		return nil, err
	}
	if len(rows) < 2 {
		return nil, nil
	}

	headers := rows[0]
	byStudent := make(map[string]db.Submission)

	for rIdx := 1; rIdx < len(rows); rIdx++ {
		row := rows[rIdx]
		if isRowEmpty(row) {
			continue
		}
		rowMap := make(map[string]string)
		for cIdx, h := range headers {
			hClean := strings.TrimSpace(h)
			if hClean == "" {
				continue
			}
			val := ""
			if cIdx < len(row) {
				val = strings.TrimSpace(row[cIdx])
			}
			rowMap[hClean] = val
		}

		sid, sName, sEmail := resolveStudentIdentity(rowMap, rosterByID, rosterList)
		if sid == "" {
			continue
		}

		// Ensure student exists in studentsMap
		st, exists := studentsMap[sid]
		if !exists {
			if sName == "" {
				sName = "Student " + sid
			}
			st = db.Student{
				ID:               sid,
				Name:             cleanName(sName),
				Email:            sEmail,
				EnrollmentStatus: "Enrolled",
			}
		} else {
			if (st.Name == "" || strings.HasPrefix(st.Name, "Student ")) && sName != "" {
				st.Name = cleanName(sName)
			}
			if st.Email == "" && sEmail != "" {
				st.Email = sEmail
			}
		}
		studentsMap[sid] = st

		sub := buildSubmission(hw.Number, def, sid, st.Name, rowMap, baseDir, dataDir, localIndex)
		if prev, ok := byStudent[sid]; ok {
			sub.AttemptCount = prev.AttemptCount + 1
			// Keep existing embed/urls if latest attempt was empty
			if sub.PrimaryURL == "" {
				sub.PrimaryURL = prev.PrimaryURL
			}
			if sub.EmbedURL == "" {
				sub.EmbedURL = prev.EmbedURL
				sub.Playable = prev.Playable
			}
		}
		byStudent[sid] = sub
	}

	var out []db.Submission
	for _, sub := range byStudent {
		out = append(out, sub)
	}
	sort.Slice(out, func(i, j int) bool {
		return out[i].StudentID < out[j].StudentID
	})
	return out, nil
}

func resolveStudentIdentity(row map[string]string, rosterByID map[string]RosterSeedEntry, rosterList []RosterSeedEntry) (id, name, email string) {
	var rawID, firstName, lastName, fullName string
	for k, v := range row {
		kl := strings.ToLower(k)
		switch {
		case kl == "email address" || kl == "heuser email":
			if v != "" && email == "" {
				email = v
			}
		case strings.Contains(kl, "first name"):
			firstName = v
		case strings.Contains(kl, "last name") || strings.Contains(kl, "second/last"):
			lastName = v
		case kl == "full name":
			fullName = v
		case strings.Contains(kl, "student id") || strings.Contains(kl, "heuser id"):
			rawID = v
		}
	}

	if fullName == "" {
		fullName = strings.TrimSpace(firstName + " " + lastName)
	}

	// 1. Check email for exact 10-digit Heuser ID (202801XXXX)
	if m := reFullID.FindString(email); m != "" {
		id = m
	}

	// 2. Parse numeric/scientific notation ID from rawID
	parsedRawID := normalizeIDString(rawID)
	if id == "" && reFullID.MatchString(parsedRawID) {
		id = reFullID.FindString(parsedRawID)
	}

	// 3. Match 3-digit suffix (or partial ID) against rosterList using name similarity
	if id == "" && parsedRawID != "" {
		suffix := parsedRawID
		if len(suffix) < 3 {
			suffix = strings.Repeat("0", 3-len(suffix)) + suffix
		}
		var matches []RosterSeedEntry
		for _, r := range rosterList {
			if r.ID != "" && strings.HasSuffix(r.ID, suffix) {
				matches = append(matches, r)
			}
		}
		if len(matches) == 1 {
			id = matches[0].ID
		} else if len(matches) > 1 {
			bestScore := -1
			for _, m := range matches {
				sc := nameOverlapScore(fullName, m.Name)
				if sc > bestScore {
					bestScore = sc
					id = m.ID
				}
			}
		}
	}

	// 4. Fallback: match by fullName against rosterList
	if id == "" && fullName != "" {
		bestScore := 0
		for _, r := range rosterList {
			sc := nameOverlapScore(fullName, r.Name)
			if sc > bestScore {
				bestScore = sc
				id = r.ID
			}
		}
		if bestScore < 2 {
			id = ""
		}
	}

	if id == "" && parsedRawID != "" {
		id = parsedRawID
	}
	if id == "" && email != "" {
		id = strings.Split(email, "@")[0]
	}

	if r, ok := rosterByID[id]; ok && r.Name != "" {
		name = r.Name
		if email == "" && r.Email != "" {
			email = r.Email
		}
	} else {
		name = fullName
	}
	if email == "" && reFullID.MatchString(id) {
		email = id + "@heusercollege.edu.pk"
	}
	return id, cleanName(name), email
}

func normalizeIDString(raw string) string {
	s := strings.TrimSpace(raw)
	if s == "" {
		return ""
	}
	if strings.ContainsAny(s, "eE.") {
		if f, err := strconv.ParseFloat(s, 64); err == nil && f > 0 {
			return strconv.FormatInt(int64(math.Round(f)), 10)
		}
	}
	return s
}

func nameOverlapScore(a, b string) int {
	ta := strings.Fields(strings.ToLower(a))
	tb := strings.Fields(strings.ToLower(b))
	score := 0
	for _, wa := range ta {
		if len(wa) < 2 {
			continue
		}
		for _, wb := range tb {
			if wa == wb {
				score += 2
			} else if strings.HasPrefix(wb, wa) || strings.HasPrefix(wa, wb) {
				score += 1
			}
		}
	}
	return score
}

func buildSubmission(
	hwNum int,
	def HomeworkDefinition,
	sid, studentName string,
	row map[string]string,
	baseDir, dataDir string,
	localIndex []localFileEntry,
) db.Submission {
	subID := fmt.Sprintf("hw%d-%s", hwNum, sid)
	sub := db.Submission{
		ID:           subID,
		StudentID:    sid,
		HWNumber:     hwNum,
		HWTitle:      def.Title,
		HWKind:       def.Kind,
		AttemptCount: 1,
	}

	rawBytes, _ := json.Marshal(row)
	sub.RawJSON = string(rawBytes)

	var extraURLs []LabeledURL
	var feedbacks []string

	// Extract timestamp
	if ts, ok := row["Timestamp"]; ok && ts != "" {
		sub.SubmittedAt = formatExcelTimestamp(ts)
	}

	for k, v := range row {
		if v == "" {
			continue
		}
		kl := strings.ToLower(k)
		if kl == "timestamp" || kl == "email address" || kl == "heuser email" ||
			strings.Contains(kl, "first name") || strings.Contains(kl, "last name") ||
			strings.Contains(kl, "second/last") || kl == "full name" ||
			strings.Contains(kl, "student id") || strings.Contains(kl, "heuser id") {
			continue
		}

		if strings.Contains(kl, "enjoy") || strings.Contains(kl, "how hard") || strings.Contains(kl, "prefer") {
			feedbacks = append(feedbacks, fmt.Sprintf("%s: %s", k, v))
			continue
		}

		// URL / Deliverable column
		if strings.HasPrefix(strings.ToLower(v), "file:///") {
			sub.IsLocalOnlyURL = true
			if sub.PrimaryURL == "" {
				sub.PrimaryURL = v
			}
			extraURLs = append(extraURLs, LabeledURL{Label: k, URL: v})
			continue
		}

		if hwNum == 1 || hwNum == 2 {
			urls := reMakeCodeID.FindAllString(v, -1)
			if len(urls) > 0 {
				cleanURL := urls[0]
				m := reMakeCodeID.FindStringSubmatch(cleanURL)
				if len(m) > 1 {
					shareCode := m[1]
					// Normalize missing 'S' prefix on 20-digit code if needed
					if len(shareCode) == 23 && shareCode[0] >= '0' && shareCode[0] <= '9' {
						cleanURL = "https://arcade.makecode.com/S" + shareCode
						shareCode = "S" + shareCode
					}
					sub.PrimaryURL = cleanURL
					sub.EmbedURL = "https://arcade.makecode.com/---run?id=" + shareCode
					sub.Playable = true
				}
			} else if all := reAnyURL.FindAllString(v, -1); len(all) > 0 {
				sub.PrimaryURL = all[0]
			}
			extraURLs = append(extraURLs, LabeledURL{Label: k, URL: v})
			continue
		}

		// Extract all URLs in cell (also handle bare hostnames like MBilal9509.pythonanywhere.com)
		foundURLs := reAnyURL.FindAllString(v, -1)
		if len(foundURLs) == 0 {
			trimmed := strings.TrimSpace(v)
			if !strings.Contains(trimmed, " ") && (strings.Contains(trimmed, ".pythonanywhere.com") ||
				strings.Contains(trimmed, ".onrender.com") ||
				strings.Contains(trimmed, ".vercel.app") ||
				strings.Contains(trimmed, ".netlify.app") ||
				strings.Contains(trimmed, ".github.io") ||
				strings.Contains(trimmed, "wokwi.com/")) {
				foundURLs = []string{"https://" + trimmed}
			}
		}
		for _, u := range foundURLs {
			u = strings.TrimRight(u, ".,;)\u2060\u200b\ufeff")
			extraURLs = append(extraURLs, LabeledURL{Label: k, URL: u})
		}
	}

	// Categorize primary / secondary URLs for HW 4+
	if hwNum >= 4 {
		for _, eu := range extraURLs {
			u := eu.URL
			ul := strings.ToLower(u)
			if strings.HasPrefix(ul, "file:///") {
				continue
			}
			isRepo := strings.Contains(ul, "github.com/") && !strings.Contains(ul, ".github.io")
			isWokwi := strings.Contains(ul, "wokwi.com/")
			isPages := strings.Contains(ul, ".github.io") ||
				strings.Contains(ul, "onrender.com") ||
				strings.Contains(ul, "pythonanywhere.com") ||
				strings.Contains(ul, "vercel.app") ||
				strings.Contains(ul, "netlify.app")

			if hwNum == 10 {
				if isWokwi && sub.PrimaryURL == "" {
					sub.PrimaryURL = u
					sub.Playable = true
				} else if isPages && sub.SecondaryURL == "" {
					sub.SecondaryURL = u
					sub.Playable = true
				} else if !isRepo && sub.PrimaryURL == "" {
					sub.PrimaryURL = u
				} else if sub.SecondaryURL == "" && u != sub.PrimaryURL && !isRepo {
					sub.SecondaryURL = u
				}
			} else if hwNum >= 7 {
				if isPages && sub.PrimaryURL == "" {
					sub.PrimaryURL = u
					sub.Playable = true
				} else if isRepo && sub.SecondaryURL == "" {
					sub.SecondaryURL = u
				} else if sub.PrimaryURL == "" {
					sub.PrimaryURL = u
				} else if sub.SecondaryURL == "" && u != sub.PrimaryURL {
					sub.SecondaryURL = u
				}
			} else {
				if sub.PrimaryURL == "" {
					sub.PrimaryURL = u
				} else if sub.SecondaryURL == "" && u != sub.PrimaryURL {
					sub.SecondaryURL = u
				}
			}
		}
		if sub.PrimaryURL == "" && sub.SecondaryURL != "" {
			sub.PrimaryURL = sub.SecondaryURL
			sub.SecondaryURL = ""
		}
	}

	// Match local files in (File responses)
	matchedFiles := matchLocalFiles(localIndex, sid, studentName)
	var fileRefs []LocalFileRef
	for _, lf := range matchedFiles {
		fileRefs = append(fileRefs, LocalFileRef{
			Label:   lf.Label,
			RelPath: lf.RelPath,
			Kind:    lf.Kind,
		})
	}

	// For HW6, attempt to extract a playable web game from local zip/html files!
	if hwNum == 6 && len(matchedFiles) > 0 {
		if ok := prepareHW6Game(baseDir, dataDir, sid, matchedFiles); ok {
			sub.EmbedURL = fmt.Sprintf("/play/hw6/%s/", sid)
			sub.Playable = true
		}
	}

	// Deduplicate extraURLs
	euBytes, _ := json.Marshal(extraURLs)
	lfBytes, _ := json.Marshal(fileRefs)
	sub.ExtraURLsJSON = string(euBytes)
	sub.LocalFilesJSON = string(lfBytes)
	sub.Feedback = strings.Join(feedbacks, "\n")

	return sub
}

func formatExcelTimestamp(raw string) string {
	f, err := strconv.ParseFloat(raw, 64)
	if err == nil && f > 30000 {
		if t, err := excelize.ExcelDateToTime(f, false); err == nil {
			return t.Format("2006-01-02 15:04")
		}
	}
	return raw
}

func cleanName(s string) string {
	s = strings.TrimSpace(reMultiWS.ReplaceAllString(s, " "))
	if s == "" {
		return ""
	}
	words := strings.Fields(s)
	for i, w := range words {
		if len(w) == 0 {
			continue
		}
		if w == strings.ToLower(w) || w == strings.ToUpper(w) {
			words[i] = strings.ToUpper(w[:1]) + strings.ToLower(w[1:])
		}
	}
	return strings.Join(words, " ")
}

func isRowEmpty(row []string) bool {
	for _, c := range row {
		if strings.TrimSpace(c) != "" {
			return false
		}
	}
	return true
}

func DriveFileID(urlStr string) string {
	m := reDriveID.FindStringSubmatch(urlStr)
	if len(m) > 1 {
		return m[1]
	}
	return ""
}
