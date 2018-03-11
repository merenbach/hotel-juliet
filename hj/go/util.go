package main

// ziprunes creates a map from two sets of runes
// any repeats in `a` will be ignored, in effect preventing overwrites
func ziprunes(a, b []rune) map[rune]rune {
        out := make(map[rune]rune)
        for i, e := range a {
		if _, exists := out[e]; !exists {
			out[e] = b[i]
		}
        }
        return out
}

