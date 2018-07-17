package main

// Monoalphabetic substitution ciphers

import (
	"strings"
	"unicode/utf8"
)

// NewKeywordCipher creates a new keyword cipher.
func NewKeywordCipher(alphabet, keyword string) Cipher {
	ctAlphabet := deduplicateString(keyword + alphabet)
	return NewSimpleTableau(alphabet, ctAlphabet)
}

// NewAffineCipher creates a new affine cipher.
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
	ctAlphabet := backpermute(ptAlphabet, lcg.Next)

	return NewSimpleTableau(ptAlphabet, ctAlphabet)
}

// NewAtbashCipher creates a new Atbash cipher.
func NewAtbashCipher(ptAlphabet string) Cipher {
	return NewAffineCipher(ptAlphabet, -1, -1)
}

// NewCaesarCipher creates a new Caesar cipher.
func NewCaesarCipher(ptAlphabet string, b int) Cipher {
	return NewAffineCipher(ptAlphabet, 1, b)
}

// NewDecimationCipher creates a new decimation cipher.
func NewDecimationCipher(ptAlphabet string, a int) Cipher {
	return NewAffineCipher(ptAlphabet, a, 0)
}

// NewRot13Cipher creates a new Rot13 (Caesar shift of 13) cipher.
func NewRot13Cipher(ptAlphabet string) Cipher {
	return NewCaesarCipher(ptAlphabet, 13)
}

// Backpermute transforms a string based on a generator function.
// Backpermute will panic if the transform function returns any invalid string index values.
func backpermute(s string, g func() uint) string {
	var out strings.Builder
	asRunes := []rune(s)
	for range asRunes {
		newRune := asRunes[g()]
		out.WriteRune(newRune)
	}
	return out.String()
}

// Deduplicate removes recurrences for runes from a string, preserving order of first appearance.
func deduplicateString(s string) string {
	var out strings.Builder
	seen := make(map[rune]bool)

	for _, e := range []rune(s) {
		if _, ok := seen[e]; !ok {
			out.WriteRune(e)
			seen[e] = true
		}
	}
	return out.String()
}
