package main

import (
	"sort"
	"strings"
	"unicode/utf8"
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

// Chunk divides a string into groups.
func chunk(s string, size int, delimiter rune) string {
	return strings.Join(groupString(s, size, 'X'), string(delimiter))
}

// DiffToMod returns the difference between a and the nearest multiple of m.
func diffToMod(a, m int) int {
	if remainder := a % m; remainder != 0 {
		return m - remainder
	}
	return 0
}

// GroupString divides a string into groups.
func groupString(s string, size int, padding rune) []string {
	out := make([]string, 0)
	nullCount := diffToMod(utf8.RuneCountInString(s), size)
	nulls := strings.Repeat(string(padding), nullCount)
	padded := []rune(s + nulls)
	for i := 0; i < len(padded); i += size {
		out = append(out, string(padded[i:i+size]))
	}
	return out
}
