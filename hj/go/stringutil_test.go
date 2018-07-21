package main

import (
	"reflect"
	"testing"
)

func TestBackpermute(t *testing.T) {
	tables := []struct {
		expected string
		s        string
		f        func() uint
	}{
		{"eeeee", "hello", func() uint { return 1 }},
	}
	for _, table := range tables {
		if out := backpermute(table.s, table.f); out != table.expected {
			t.Errorf("for backpermutation of %q with function %s, expected output %q, but got %q instead", table.s, reflect.ValueOf(table.f), table.expected, out)
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
			t.Errorf("deduplication of string %q was %q; expected %q", k, o, v)
		}
	}
}
