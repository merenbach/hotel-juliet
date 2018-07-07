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
		tableau := NewSimpleTableau(table.pt, table.ct)
		if output := tableau.String(); output != table.expected {
			t.Errorf("Tableau printout doesn't match for PT %q and CT %q. Received: %s; expected: %s", table.pt, table.ct, output, table.expected)
		}
		if output := tableau.Encrypt(table.pt, false); output != table.ct {
			t.Errorf("Tableau Pt2Ct doesn't match for PT %q and CT %q. Received: %s", table.pt, table.ct, output)
		}
		if output := tableau.Decrypt(table.ct, false); output != table.pt {
			t.Errorf("Tableau Ct2Pt doesn't match for PT %q and CT %q. Received: %s", table.pt, table.ct, output)
		}
	}
}
