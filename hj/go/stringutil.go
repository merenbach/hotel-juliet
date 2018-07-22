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
func deduplicate(s string) string {
	var out strings.Builder
	seen := make(map[rune]bool)

	for _, r := range s {
		if _, ok := seen[r]; !ok {
			out.WriteRune(r)
			seen[r] = true
		}
	}
	return out.String()
}

// Intersect removes runes from a string if they don't occur in another string.
func intersect(s, charset string) string {
	var out strings.Builder
	seen := make(map[rune]bool)

	for _, r := range charset {
		seen[r] = true
	}

	for _, r := range s {
		if _, ok := seen[r]; ok {
			out.WriteRune(r)
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

// Chunk divides a string into groups separated by a delimiter.
func chunk(s string, size int, delimiter rune) string {
	var out strings.Builder
	for i, r := range []rune(s) {
		out.WriteRune(r)
		if i%size == size-1 && i != len(s)-1 {
			out.WriteRune(delimiter)
		}
	}
	return out.String()
}
