package main

import "strings"

// // MapRunes transforms a string by mapping runes through a function.
// func MapRunes(s string, f func(rune) rune) string {
// 	var out strings.Builder
// 	for _, r := range []rune(s) {
// 		o, found := m[r]
// 		if !found && !strict {
// 			o = r
// 		}
// 		out.WriteRune(o)
// 	}
// 	return out.String()
// }

// zipstrings creates a map from two strings (as rune arrays)
// zipstrings will panic if any runes in `a` occur more than once in `a`
// zipstrings will NOT panic if runes repeat in `b`, but often zipstrings will be invoked reciprocally
func ziprunes(a, b []rune) map[rune]rune {
	seen := make(map[rune]bool)
	out := make(map[rune]rune)
	for i, e := range a {
		if _, found := seen[e]; found {
			panic("runes may not repeat")
		}
		out[e] = b[i]
		seen[e] = true
	}
	return out
}

// Backpermute transforms a string based on a generator function.
// Backpermute will panic if the transform function returns any invalid string index values.
func Backpermute(s string, g func() int) string {
	var out strings.Builder
	asRunes := []rune(s)
	for _ = range asRunes {
		newRune := asRunes[g()]
		out.WriteRune(newRune)
	}
	return out.String()
}

// Deduplicate removes recurrences for runes from a string, preserving order of first appearance.
func Deduplicate(s string) string {
	var out strings.Builder
	seen := make(map[rune]bool)

	for _, e := range []rune(s) {
		if _, ok := seen[e]; !ok {
			out.WriteRune(e)
			seen[e] = true
		}
	}
	return out.String()
}

// TODO: document
func mapRuneTransform(xtable map[rune]rune) func(string) string {
	return func(message string) string {
		out := []rune(message)
		for i, e := range []rune(message) {
			xcoded, ok := xtable[e]
			if ok {
				out[i] = xcoded
			}
		}
		return string(out)
	}
}
