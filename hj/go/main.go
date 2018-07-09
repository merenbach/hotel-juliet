package main

//todo: strict
//todo: param groups (caesar, atbash, etc)
// TODO:
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

import (
	"fmt"
	"strings"
)

// Invert swaps indices and values in an array of integers.
// Invert panics upon encountering elements that don't represent valid indices in the source array.
// TODO: panic on duplicates?
func invert(a []int) []int {
	out := make([]int, len(a))
	for idx, elem := range a {
		out[elem] = idx
	}
	return out
}

func zipper(a, b string) ([]int, []int, error) {
	lennya := len(a)
	lennyb := len(b)
	// var out1 uint[lennya]
	// var out2 uint[lennyb]
	out1 := make([]int, lennya)
	out2 := make([]int, lennyb)
	for idx, char := range b {
		if idxOfBInA := strings.IndexRune(a, char); idxOfBInA != (-1) {
			out1[idx] = idxOfBInA
			out2[idxOfBInA] = idx
		} else {
			return nil, nil, fmt.Errorf("character sets did not match")
		}
	}
	return out1, out2, nil
}

func main() {
	fmt.Println("Hello, world!")
	alphabet := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	// alphabet2 := "DEFGHIJKLMNOPQRSTUVWXYZABC"
	// THE MATH IS BEAUTIFUL... but.... it makes no sense to look up rune
	// positions in other strings, convert, and convert back, in O(2n),
	// when we could use maps of runes in O(1) or O(2).
	// A table is how it would be done by hand, rather than calculating each time.
	// So use a map!
	// t := MakeTableau(alphabet, "", func(i int) int {
	// 	return (i + 3) % len(alphabet)
	// })
	// t := MakeSimpleTableau(alphabet, alphabet2)
	// fmt.Println(t)
	// fmt.Println("E:", t.Encrypt("HELLO, WORLD", true))
	// fmt.Println("D:", t.Decrypt("KHOOR, ZRUOG", false))
	t := NewAtbashCipher(alphabet)
	// t = MakeSimpleTableauFromFunc(alphabet, func(i int) int {
	// 	return (i + 3) % len(alphabet)
	// })
	fmt.Println(t)
	fmt.Println("E:", t.Encrypt("HELLO, WORLD", true))
	fmt.Println("E:", t.Decrypt("SVOOL, DLIOW", true))
	fmt.Println("D:", t.Decrypt("KHOOR, ZRUOG", false))
	// fmt.Println(t.Pt2Ct("HELLOWORLD"))
	// fmt.Println(t.Ct2Pt("KHOORZRUOG"))

	// ct := []int{3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0, 1, 2}
	// ct_inverse := invert(ct)
	// ab1 := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	// for _, n := range ct {
	// 	fmt.Printf(string(ab1[ct_inverse[n]]))

	// }
	// fmt.Println()
	// for idx, _ := range ct {
	// 	fmt.Printf(string(ab1[ct[idx]]))

	// }
	// fmt.Println()
	// fmt.Println(ct)
	// fmt.Println(ct_inverse)
	// // ab1 := "ABCDEFGHIJKLMNOPQRSTUVWXYZ
	// // ab2 := "DEFGHIJKLMNOPQRSTUVWXYZABC"
	// // fmt.Println(zipper(ab1, ab2))
	// // ab2 = "EFGHIJKLMNOPQRSTUVWXYZABCd"
	// // fmt.Println(zipper(ab1, ab2))
	// t2 := NewTabulaRecta(alphabet, alphabet, alphabet)
	// fmt.Println(t2)
	// fmt.Println(t2.Encrypt("THIS IS MY VOICE", "SOCRATES", false))
	// fmt.Println(t2.Decrypt("VGPLB, KUILS!", "OCEANOGRAPHYWHAT", true))
	t3 := NewBeaufortCipher(alphabet)
	fmt.Println(t3)
	o := t3.Encrypt("HELLO, WORLD", "OCEANOGRAPHYWHAT", false)
	// o := t3.Encrypt("HYTPZ, SSAPM!", "OCEANOGRAPHYWHAT", false)
	fmt.Println("this is it: ", o)
	fmt.Println("hey", t3.Encrypt(o, "OCEANOGRAPHYWHAT", false))
	// HYTPZ, SSAPM!
}
