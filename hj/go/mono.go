package main

// Simple (one glyph at a time) monoalphabetic substitution ciphers

import (
	"unicode/utf8"
)

// NewKeywordCipher creates a new keyword cipher.
func NewKeywordCipher(alphabet, keyword string) Cipher {
	ctAlphabet := Deduplicate(keyword + alphabet)
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
	ctAlphabet := Backpermute(ptAlphabet, lcg.Next)

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
