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

