package main

// TODO: question: can we do an encipherRune for pasc? something something key advancement closure mumble mumble something?
//todo: strict
//todo: param groups (caesar, atbash, etc)
// TODO:
//  * return runes from all ciphers, and only convert to strings in message?
//  * additional unit tests, esp. with int'l charsets
//  * documentation
//  * formatting
//  * strict mode: on new Message struct type
//  * multicase alphabets?
//  * multi value returns (e.g., out, error)
//  * keyword cipher
//  * polyalphabetic ciphers
//  * should we use pointers instead of values after all?... (probably not)
//  * clean up method/function names
//  * re-explore Message struct type for chaining
//  * add tests for more util funcs and LCG
//  * add more informative documentation
//  * explore use of tabwriter for tabula recta, tableau printing
//  * tabula recta seems inefficient converting runes to strings each time
//  * explore ways to make backpermute more easily testable, or explore ways to replace it
//  * --> backpermute should probably take an int slice, so when using the LCG we'd
//        want a consumer method of some sort that goes out to the length of the string being permuted
//  * print key attached to tabula recta when displaying tabula recta, or don't require key in init (for Trithemius, maybe use closure or partial application to avoid needing key immediately?)

import (
	"fmt"
)

// A Cipher implementation can encipher and decipher strings.
// TODO: should `strict` be in creation, not Encipher/Decipher?
type Cipher interface {
	String() string
	Encipher(string, bool) string
	Decipher(string, bool) string
}

// not needed if we're returning a Cipher from the func, thanks to static typing
// var _ Cipher = NewAtbashCipher()

// // Invert swaps indices and values in an array of integers.
// // Invert panics upon encountering elements that don't represent valid indices in the source array.
// // TODO: panic on duplicates?
// func invert(a []int) []int {
// 	out := make([]int, len(a))
// 	for idx, elem := range a {
// 		out[elem] = idx
// 	}
// 	return out
// }

// func zipper(a, b string) ([]int, []int, error) {
// 	lennya := len(a)
// 	lennyb := len(b)
// 	// var out1 uint[lennya]
// 	// var out2 uint[lennyb]
// 	out1 := make([]int, lennya)
// 	out2 := make([]int, lennyb)
// 	for idx, char := range b {
// 		if idxOfBInA := strings.IndexRune(a, char); idxOfBInA != (-1) {
// 			out1[idx] = idxOfBInA
// 			out2[idxOfBInA] = idx
// 		} else {
// 			return nil, nil, fmt.Errorf("character sets did not match")
// 		}
// 	}
// 	return out1, out2, nil
// }

func main() {
	fmt.Println("Hello, world!")
}
