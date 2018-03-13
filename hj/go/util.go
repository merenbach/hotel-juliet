package main

// ziprunes creates a map from two sets of runes
// TODO: any repeats in `a` should be ignored, in effect preventing overwrites
func ziprunes(a, b []rune) map[rune]rune {
	out := make(map[rune]rune)
	for i, e := range []rune(a) {
		out[e] = b[i]
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
