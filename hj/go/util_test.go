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
