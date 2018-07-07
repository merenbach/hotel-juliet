package main

import (
	"math/big"
	"unicode/utf8"
)

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

// BELOW IS ALL OLD STUFF; PLEASE REMOVE

// TODO: Needs error option or ok option
// affine returns the result of `(ax + b) mod m`
// TODO: enforce constraints such as m > 0
// https://en.wikipedia.org/wiki/Linear_congruential_generator
func makeAffine(m, a, b int) func() *big.Int {
	m_, a_, b_ := int64(m), int64(a), int64(b)
	// TODO: consider using Hull-Dobell satisfaction to determine if `a` is valid (must be coprime with `m`)
	f, _ := makeLCG(big.NewInt(m_), big.NewInt(1), big.NewInt(a_), big.NewInt(b_))
	return f
}

func makeAffineTableau(alphabet string, a, b int) tableau {
	ptAlphabet := removeRuneDuplicates([]rune(alphabet))
	myfn := makeAffine(len(ptAlphabet), a, b)
	ctAlphabet := removeRuneDuplicates(affineTransform(ptAlphabet, myfn))
	return tableau{string(ptAlphabet), string(ctAlphabet)}
}

func MakeAffineEncrypt(alphabet string, a, b int) func(string) string {
	tableau := makeAffineTableau(alphabet, a, b)
	return tableau.Pt2Ct()
}

func MakeAffineDecrypt(alphabet string, a, b int) func(string) string {
	tableau := makeAffineTableau(alphabet, a, b)
	return tableau.Ct2Pt()
}

func MakeAtbashEncrypt(alphabet string) func(string) string {
	ab := len([]rune(alphabet)) - 1
	return MakeAffineEncrypt(alphabet, ab, ab)
}
func MakeAtbashDecrypt(alphabet string) func(string) string {
	ab := len([]rune(alphabet)) - 1
	return MakeAffineDecrypt(alphabet, ab, ab)
}

func Affine(a, b, m int) func() int {
	// m_, a_, b_ := int64(m), int64(a), int64(b)
	// TODO: consider using Hull-Dobell satisfaction to determine if `a` is valid (must be coprime with `m`)
	for a < 0 {
		a += m
	}
	for b < 0 {
		b += m
	}
	aff, _ := makeLCG2(m, 1, a, b)
	return aff
}
func Atbash(m int) func() int {
	return Affine(-1, -1, m)
}
func Caesar(b int, m int) func() int {
	return Affine(1, b, m)
}
func Decimation(a int, m int) func() int {
	return Affine(a, 0, m)
}
func Rot13(m int) func() int {
	return Caesar(13, m)
}

func MakeCaesarEncrypt(alphabet string, b int) func(string) string {
	return MakeAffineEncrypt(alphabet, 1, b)
}
func MakeCaesarDecrypt(alphabet string, b int) func(string) string {
	return MakeAffineDecrypt(alphabet, 1, b)
}

func MakeDecimationEncrypt(alphabet string, a int) func(string) string {
	return MakeAffineEncrypt(alphabet, a, 0)
}
func MakeDecimationDecrypt(alphabet string, a int) func(string) string {
	return MakeAffineDecrypt(alphabet, a, 0)
}

func MakeRot13Encrypt(alphabet string) func(string) string {
	return MakeCaesarEncrypt(alphabet, 13)
}
func MakeRot13Decrypt(alphabet string) func(string) string {
	return MakeCaesarDecrypt(alphabet, 13)
}

// transform transforms a rune array (alphabet) based on a function
func affineTransform(alphabet []rune, fn func() *big.Int) []rune {
	out := make([]rune, 0)
	for range alphabet {
		pos := fn().Int64()
		out = append(out, alphabet[pos])
	}
	return out
}
