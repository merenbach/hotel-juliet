package main

import "testing"

func TestTableau(t *testing.T) {

	tables := []struct {
		pt       string
		ct       string
		expected string
	}{
		{"ABCDE", "DEFGH", "PT: ABCDE\nCT: DEFGH"},
		{"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "DEFGHIJKLMNOPQRSTUVWXYZABC", "PT: ABCDEFGHIJKLMNOPQRSTUVWXYZ\nCT: DEFGHIJKLMNOPQRSTUVWXYZABC"},
	}
	for _, table := range tables {
		tableau := tableau{table.pt, table.ct}
		if output := tableau.String(); output != table.expected {
			t.Errorf("Tableau printout doesn't match for PT \"%s\" and CT \"%s\". Received: %s; expected: %s", table.pt, table.ct, output, table.expected)
		}
		if output := tableau.Pt2Ct()(table.pt); output != table.ct {
			t.Errorf("Tableau Pt2Ct doesn't match for PT \"%s\" and CT \"%s\". Received: %s", table.pt, table.ct, output)
		}
		if output := tableau.Ct2Pt()(table.ct); output != table.pt {
			t.Errorf("Tableau Ct2Pt doesn't match for PT \"%s\" and CT \"%s\". Received: %s", table.pt, table.ct, output)
		}
	}
}
