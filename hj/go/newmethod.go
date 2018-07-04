package main

import (
	"fmt"
	"log"
	"strings"
)

func runePositionsOfString(needle, haystack string) []int {
	out := make([]int, len([]rune(needle)))
	for idx, r := range []rune(needle) {
		out[idx] = strings.IndexRune(haystack, r)
	}
	return out
}

func revarray(positions []int) ([]int, error) {
	out := make([]int, len(positions))
	for idx, element := range positions {
		if element < 0 || element >= len(out) {
			return nil, fmt.Errorf("element %d out of bounds 0 <= x < %d", element, len(out))
		}
		out[element] = idx
	}
	return out, nil
}

// func encode(s, alphabet string, xtable []int) string {
// 	for c := range []rune(s) {

// 	}
// }

func main() {
	fmt.Println("vim-go")
	alphabet := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	message := "MEET AT NOON my FRIEND"
	positions := runePositionsOfString(message, alphabet)
	fmt.Println(positions)

	ctAlphabet := "DEFGHIJKLMNOPQRSTUVWXYZABC"
	// TODO: instead of the NEXT LINE, start with an array 0..25 and manipulate it as necessary;
	// the next line will be useful for non-math variants such as the keyword cipher
	// at that point, the actual string conversion (A=>0, Z=>25, 0=>D, 25=>C, etc.)
	// become "layer 6"--presentation layer only.
	// Thus outside of input and output, we use _only_ numbers.
	a := runePositionsOfString(ctAlphabet, alphabet)
	fmt.Println(a)
	a = []int{3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0, 1, 2}
	b, err := revarray(a)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("a = ", a)
	fmt.Println("b = ", b)
}
