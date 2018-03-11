package main

import (
	"fmt"
	"math/big"
)


// TODO: Needs error option or ok option
// affine returns the result of `(ax + b) mod m`
// TODO: enforce constraints such as m > 0
// https://en.wikipedia.org/wiki/Linear_congruential_generator
func makeAffine(m, a, b int) (func() *big.Int) {
	m_, a_, b_ := int64(m), int64(a), int64(b)
	// TODO: consider using Hull-Dobell satisfaction to determine if `a` is valid (must be coprime with `m`)
	f, _ := makeLCG(big.NewInt(m_), big.NewInt(1), big.NewInt(a_), big.NewInt(b_))
	return f
}

/*func affine(x, a, b, m int) int {
	return Modulus(a * x + b, m)
}

func invaffine(x, a, b, m int) int {
	modinv := mulinv(a, m)
	return Modulus(modinv * (x - b), m)
}/*

/*type Cipher interface {
    encrypt() string
    decrypt() string
}*/

type affineCipher struct {
	ptAlphabet string
	ctAlphabet string
	a int
	b int
}

func MakeAffineCipher(alphabet string, a, b int) affineCipher {
	ptAlphabet := removeRuneDuplicates([]rune(alphabet))
	myfn := makeAffine(len(ptAlphabet), a, b)
	ctAlphabet := removeRuneDuplicates(affineTransform(ptAlphabet, myfn))
	return affineCipher{string(ptAlphabet), string(ctAlphabet), a, b}
}

func MakeAtbashCipher(alphabet string) affineCipher {
	ab := len([]rune(alphabet)) - 1
	return MakeAffineCipher(alphabet, ab, ab)
}

func MakeCaesarCipher(alphabet string, b int) affineCipher {
	return MakeAffineCipher(alphabet, 1, b)
}

func MakeDecimationCipher(alphabet string, a int) affineCipher {
	return MakeAffineCipher(alphabet, a, 0)
}

func MakeRot13Cipher(alphabet string) affineCipher {
	return MakeCaesarCipher(alphabet, 13)
}

/*
func (cipher affineCipher) transcode(message string, fn func (int, int, int, int) int) string {
	out := make([]rune, len(message))
	for _, rn := range []rune(message) {
		runeindex := strings.IndexRune(cipher.alphabet, rn)
		if runeindex != -1 {
			pos := fn(runeindex, cipher.a, cipher.b, len(cipher.alphabet))
			outrune := rune(cipher.alphabet[pos])
			out = append(out, outrune)
		}
	}
	return string(out)
}*/

// transform transforms a rune array (alphabet) based on a function
func affineTransform(alphabet []rune, fn func () *big.Int) []rune {
	out := make([]rune, 0)
	for range alphabet {
		pos := fn().Int64()
		out = append(out, alphabet[pos])
	}
	return out
}

func (cipher affineCipher) transcode(message string, xtable map[rune]rune) string {
	out := make([]rune, 0)
	for _, rn := range []rune(message) {
		xcoded, ok := xtable[rn]
		if !ok {
			xcoded = rn
		}
		out = append(out, xcoded)
	}
	return string(out)
}

func (cipher affineCipher) Encrypt(message string) string {
	xtable := ziprunes([]rune(cipher.ptAlphabet), []rune(cipher.ctAlphabet))
	return cipher.transcode(message, xtable)
}

func (cipher affineCipher) Decrypt(message string) string {
	xtable := ziprunes([]rune(cipher.ctAlphabet), []rune(cipher.ptAlphabet))
	return cipher.transcode(message, xtable)
}

func (cipher affineCipher) String() string {
	return fmt.Sprintf("Affine Cipher (ptAlphabet = %s, ctAlphabet = %s, a = %d, b = %d)", cipher.ptAlphabet, cipher.ctAlphabet, cipher.a, cipher.b)
}
