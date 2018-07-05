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
//  * also do interface, maybe, for enc/decrypt since not everything is affine based or monoalphabetic

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
	ct := []int{3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0, 1, 2}
	ct_inverse := invert(ct)
	ab1 := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	for _, n := range ct {
		fmt.Printf(string(ab1[ct_inverse[n]]))

	}
	fmt.Println()
	for idx, _ := range ct {
		fmt.Printf(string(ab1[ct[idx]]))

	}
	fmt.Println()
	fmt.Println(ct)
	fmt.Println(ct_inverse)
	// ab1 := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	// ab2 := "DEFGHIJKLMNOPQRSTUVWXYZABC"
	// fmt.Println(zipper(ab1, ab2))
	// ab2 = "EFGHIJKLMNOPQRSTUVWXYZABCd"
	// fmt.Println(zipper(ab1, ab2))
}
