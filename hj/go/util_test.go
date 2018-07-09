package main

import "testing"

func TestWrapString(t *testing.T) {
	tables := []struct {
		s        string
		i        int
		expected string
	}{
		{"hello", 3, "lohel"},
		{"hello world", 0, "hello world"},
		{"hello world", 11, "hello world"},
	}
	for _, table := range tables {
		if o := wrapString(table.s, table.i); o != table.expected {
			t.Errorf("Wrapping of string %q by %d places was %q; expected %q", table.s, table.i, o, table.expected)
		}
	}
}

func TestReverseString(t *testing.T) {
	table := map[string]string{
		"hello": "olleh",
		"world": "dlrow",
	}

	for k, v := range table {
		if o := reverseString(k); o != v {
			t.Errorf("Reverse of string %q was %q; expected %q", k, o, v)
		}
	}
}

func TestDeduplicateString(t *testing.T) {
	table := map[string]string{
		"hello":       "helo",
		"world":       "world",
		"hello world": "helo wrd",
	}

	for k, v := range table {
		if o := deduplicateString(k); o != v {
			t.Errorf("Deduplication of string %q was %q; expected %q", k, o, v)
		}
	}
}

// func TestBackpermute(t *testing.T) {
// 	t.Error("Missing test!")

// 	// tables := []struct {
// 	// 	s        string
// 	// 	f        func(int) int
// 	// 	expected string
// 	// }{
// 	// 	{"ABCDE", func(int)int{
// 	// 	},
// 	// 	{"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "DEFGHIJKLMNOPQRSTUVWXYZABC", "PT: ABCDEFGHIJKLMNOPQRSTUVWXYZ\nCT: DEFGHIJKLMNOPQRSTUVWXYZABC"},
// 	// }
// 	// for _, table := range tables {
// 	// 	tableau := tableau{table.pt, table.ct}
// 	// 	if output := tableau.String(); output != table.expected {
// 	// 		t.Errorf("Tableau printout doesn't match for PT %q and CT %q. Received: %s; expected: %s", table.pt, table.ct, output, table.expected)
// 	// 	}
// 	// 	if output := tableau.Pt2Ct()(table.pt); output != table.ct {
// 	// 		t.Errorf("Tableau Pt2Ct doesn't match for PT %q and CT %q. Received: %s", table.pt, table.ct, output)
// 	// 	}
// 	// 	if output := tableau.Ct2Pt()(table.ct); output != table.pt {
// 	// 		t.Errorf("Tableau Ct2Pt doesn't match for PT %q and CT %q. Received: %s", table.pt, table.ct, output)
// 	// 	}
// 	// }
// }
