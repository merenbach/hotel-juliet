package main

import "math/big"

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

func makeAffineAlphabets(alphabet string, a, b int) ([]rune, []rune) {
	ptAlphabet := removeRuneDuplicates([]rune(alphabet))
	myfn := makeAffine(len(ptAlphabet), a, b)
	ctAlphabet := removeRuneDuplicates(affineTransform(ptAlphabet, myfn))
	return ptAlphabet, ctAlphabet
}

func MakeAffineEncrypt(alphabet string, a, b int) func(string) string {
	ptAlphabet, ctAlphabet := makeAffineAlphabets(alphabet, a, b)
	xtable := ziprunes(ptAlphabet, ctAlphabet)
	return func(message string) string {
		return mapRuneTransform(message, xtable)
	}
}

func MakeAffineDecrypt(alphabet string, a, b int) func(string) string {
	ptAlphabet, ctAlphabet := makeAffineAlphabets(alphabet, a, b)
	xtable := ziprunes(ctAlphabet, ptAlphabet)
	return func(message string) string {
		return mapRuneTransform(message, xtable)
	}
}

func MakeAtbashEncrypt(alphabet string) func(string) string {
	ab := len([]rune(alphabet)) - 1
	return MakeAffineEncrypt(alphabet, ab, ab)
}
func MakeAtbashDecrypt(alphabet string) func(string) string {
	ab := len([]rune(alphabet)) - 1
	return MakeAffineDecrypt(alphabet, ab, ab)
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
