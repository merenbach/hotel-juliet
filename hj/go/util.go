package main

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

// remove string duplicates, preserving order of first appearance
func removeRuneDuplicates(runes []rune) []rune {
	out := make([]rune, 0)
	seen := make(map[rune]bool)

	for _, e := range runes {
		if _, ok := seen[e]; !ok {
			out = append(out, e)
			seen[e] = true
		}
	}
	return out
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
