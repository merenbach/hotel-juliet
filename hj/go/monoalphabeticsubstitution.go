package main

import (
	"unicode/utf8"
)

func NewKeywordCipher(alphabet, keyword string) Cipher {
	ctAlphabet := Deduplicate(keyword + alphabet)
	return NewSimpleTableau(alphabet, ctAlphabet)
}

// TODO: cleanup these docs and add some errors
// affine returns the result of `(ax + b) mod m`
// TODO: enforce constraints such as m > 0
// https://en.wikipedia.org/wiki/Linear_congruential_generator
func NewAffineCipher(ptAlphabet string, a, b int) Cipher {
	m := utf8.RuneCountInString(ptAlphabet)

	// TODO: consider using Hull-Dobell satisfaction to determine if `a` is valid (must be coprime with `m`)
	for a < 0 {
		a += m
	}
	for b < 0 {
		b += m
	}

	lcg := NewLCG(uint(m), 1, uint(a), uint(b))
	ctAlphabet := Backpermute(ptAlphabet, lcg.Next)

	return NewSimpleTableau(ptAlphabet, ctAlphabet)
}

func NewAtbashCipher(ptAlphabet string) Cipher {
	return NewAffineCipher(ptAlphabet, -1, -1)
}

func NewCaesarCipher(ptAlphabet string, b int) Cipher {
	return NewAffineCipher(ptAlphabet, 1, b)
}

func NewDecimationCipher(ptAlphabet string, a int) Cipher {
	return NewAffineCipher(ptAlphabet, a, 0)
}

func NewRot13Cipher(ptAlphabet string) Cipher {
	return NewCaesarCipher(ptAlphabet, 13)
}
