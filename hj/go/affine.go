package main

import (
	"unicode/utf8"
)

// TODO: cleanup these docs and add some errors
// affine returns the result of `(ax + b) mod m`
// TODO: enforce constraints such as m > 0
// https://en.wikipedia.org/wiki/Linear_congruential_generator
func MakeSimpleTableauForAffine(ptAlphabet string, a, b int) Cipher {
	m := utf8.RuneCountInString(ptAlphabet)

	// TODO: consider using Hull-Dobell satisfaction to determine if `a` is valid (must be coprime with `m`)
	for a < 0 {
		a += m
	}
	for b < 0 {
		b += m
	}
	aff, _ := makeLCG2(m, 1, a, b)

	ctAlphabet := Backpermute(ptAlphabet, aff)

	return MakeSimpleTableau(ptAlphabet, ctAlphabet)
}

func MakeSimpleTableauForAtbash(ptAlphabet string) Cipher {
	return MakeSimpleTableauForAffine(ptAlphabet, -1, -1)
}

func MakeSimpleTableauForCaesar(ptAlphabet string, b int) Cipher {
	return MakeSimpleTableauForAffine(ptAlphabet, 1, b)
}

func MakeSimpleTableauForDecimation(ptAlphabet string, a int) Cipher {
	return MakeSimpleTableauForAffine(ptAlphabet, a, 0)
}

func MakeSimpleTableauForRot13(ptAlphabet string) Cipher {
	return MakeSimpleTableauForCaesar(ptAlphabet, 13)
}
