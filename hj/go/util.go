package main

import (
	"sort"
)

// WrapString wraps a string a specified number of indices.
// WrapString will error out if the provided offset is negative.
func wrapString(s string, i int) string {
	// if we simply `return s[i:] + s[:i]`, we're operating on bytes, not runes
	u := []rune(s)
	v := append(u[i:], u[:i]...)
	return string(v)
}

// ReverseString reverses the runes in a string.
func reverseString(s string) string {
	r := []rune(s)
	sort.SliceStable(r, func(i, j int) bool {
		return true
	})
	return string(r)
}

// zipstrings creates a map from two strings (as rune arrays)
// zipstrings will panic if any runes in `a` occur more than once in `a`
// zipstrings will NOT panic if runes repeat in `b`, but often zipstrings will be invoked reciprocally
// func ziprunes(a, b []rune) map[rune]rune {
// 	seen := make(map[rune]bool)
// 	out := make(map[rune]rune)
// 	for i, e := range a {
// 		if _, found := seen[e]; found {
// 			panic("runes may not repeat")
// 		}
// 		out[e] = b[i]
// 		seen[e] = true
// 	}
// 	return out
// }

// // TODO: document
// func mapRuneTransform(xtable map[rune]rune) func(string) string {
// 	return func(message string) string {
// 		out := []rune(message)
// 		for i, e := range []rune(message) {
// 			xcoded, ok := xtable[e]
// 			if ok {
// 				out[i] = xcoded
// 			}
// 		}
// 		return string(out)
// 	}
// }
