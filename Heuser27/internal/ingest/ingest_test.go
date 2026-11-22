package ingest

import "testing"

func TestNormalizeIDString(t *testing.T) {
	cases := []struct {
		in   string
		want string
	}{
		{"2028010663", "2028010663"},
		{"2.028010663E9", "2028010663"},
		{"705.0", "705"},
		{"049", "049"},
		{"", ""},
	}
	for _, tc := range cases {
		if got := normalizeIDString(tc.in); got != tc.want {
			t.Errorf("normalizeIDString(%q) = %q, want %q", tc.in, got, tc.want)
		}
	}
}

func TestResolveStudentIdentityEdgeCases(t *testing.T) {
	rosterList := []RosterSeedEntry{
		{ID: "2028010847", Name: "Hussain Juzar", Batch: "Batch A"},
		{ID: "2028011049", Name: "Ayaan Khan", Batch: "Batch A"},
		{ID: "2028010449", Name: "Ramsha Qutaiba", Batch: "Batch A"},
		{ID: "2028011201", Name: "Muhammad Sohaib Saqib", Batch: "Batch A"},
	}
	rosterByID := map[string]RosterSeedEntry{}
	for _, r := range rosterList {
		rosterByID[r.ID] = r
	}

	// Case 1: Malformed scientific ID 2.02801847E8 but email has exact 2028010847
	id, name, _ := resolveStudentIdentity(map[string]string{
		"Email Address": "2028010847@heusercollege.edu.pk",
		"First Name":    "Hussain",
		"Last Name":     "Juzar",
		"Heuser ID":     "2.02801847E8",
	}, rosterByID, rosterList)
	if id != "2028010847" || name != "Hussain Juzar" {
		t.Fatalf("got (%q, %q), want (2028010847, Hussain Juzar)", id, name)
	}

	// Case 2: 3-digit suffix 049 ambiguous between 2028011049 and 2028010449 -> disambiguated by name
	id, name, _ = resolveStudentIdentity(map[string]string{
		"Full name":                    "Ayaan Khan",
		"Student ID (Last 3 Digits)":   "049",
	}, rosterByID, rosterList)
	if id != "2028011049" || name != "Ayaan Khan" {
		t.Fatalf("got (%q, %q), want (2028011049, Ayaan Khan)", id, name)
	}
}

func TestMakeCodeURLRegex(t *testing.T) {
	messy := "https://arcade.makecode.com/S9297https://arcade.makecode.com/S92974-51927-49918-48870https://arcade.makecode.com/S92974-51927-49918-488704-51927-49918-48870"
	m := reMakeCodeID.FindStringSubmatch(messy)
	if len(m) < 2 || m[1] != "S92974-51927-49918-48870" {
		t.Fatalf("expected S92974-51927-49918-48870, got %v", m)
	}
}
