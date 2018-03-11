package main
import "fmt"

// ziprunes creates a map from two sets of runes
// any repeats in `a` will be ignored, in effect preventing overwrites
func ziprunes(a, b []rune) map[rune]rune {
        out := make(map[rune]rune)
        for i, e := range a {
		if _, exists := out[e]; !exists {
fmt.Println("e, i = ", string(e), i)
			out[e] = b[len(out)]
		}
        }
        return out
}

