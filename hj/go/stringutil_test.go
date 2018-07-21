package main

import (
	"fmt"
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
			t.Errorf("For backpermutation of %q with function %s, expected output %q, but got %q instead", table.s, reflect.ValueOf(table.f), table.expected, out)
		}
	}
}

func TestDeduplicate(t *testing.T) {
	table := map[string]string{
		"hello":       "helo",
		"world":       "world",
		"hello world": "helo wrd",
	}

	for k, v := range table {
		if o := deduplicate(k); o != v {
			t.Errorf("Deduplication of string %q was %q; expected %q", k, o, v)
		}
	}
}

func TestIntersect(t *testing.T) {
	tables := [][]string{
		{"HELLO, WORLD!", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "HELLOWORLD"},
		{"world", "word", "word"},
		{"world", "hello", "ol"},
		{"hello", "world", "llo"},
	}

	for _, table := range tables {
		if o := intersect(table[0], table[1]); o != table[2] {
			t.Errorf("Intersection of string %q with charset %q was %q; expected %q", table[0], table[1], o, table[2])
		}
	}
}

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

func ExampleWrapString() {
	s := "HELLO,_WORLD!"
	for i := range []rune(s) {
		fmt.Println(wrapString(s, i))
	}
	// Output:
	// HELLO,_WORLD!
	// ELLO,_WORLD!H
	// LLO,_WORLD!HE
	// LO,_WORLD!HEL
	// O,_WORLD!HELL
	// ,_WORLD!HELLO
	// _WORLD!HELLO,
	// WORLD!HELLO,_
	// ORLD!HELLO,_W
	// RLD!HELLO,_WO
	// LD!HELLO,_WOR
	// D!HELLO,_WORL
	// !HELLO,_WORLD
}
