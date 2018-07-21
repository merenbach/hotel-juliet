package main

import (
	"sort"
	"strings"
)

// Backpermute transforms a string based on a generator function.
// Backpermute will panic if the transform function returns any invalid string index values.
func backpermute(s string, g func() uint) string {
	var out strings.Builder
	asRunes := []rune(s)
	for range asRunes {
		newRune := asRunes[g()]
		out.WriteRune(newRune)
	}
	return out.String()
}

// Deduplicate removes recurrences for runes from a string, preserving order of first appearance.
func deduplicateString(s string) string {
	var out strings.Builder
	seen := make(map[rune]bool)

	for _, e := range s {
		if _, ok := seen[e]; !ok {
			out.WriteRune(e)
			seen[e] = true
		}
	}
	return out.String()
}

// ReverseString reverses the runes in a string.
func reverseString(s string) string {
	r := []rune(s)
	sort.SliceStable(r, func(i, j int) bool {
		return true
	})
	return string(r)
}
