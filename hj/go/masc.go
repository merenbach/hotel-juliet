package main

// Monoalphabetic substitution ciphers

import (
	"fmt"
	"strings"
	"unicode/utf8"
)

// A SimpleSubstitutionCipher represents a simple monoalphabetic substitution cipher.
type simpleSubstitutionCipher struct {
	ptAlphabet string
	ctAlphabet string

	pt2ct map[rune]rune
	ct2pt map[rune]rune
}

// NewSimpleSubstitutionCipher creates a reciprocal, monoalphabetic substitution cipher.
func NewSimpleSubstitutionCipher(ptAlphabet string, ctAlphabet string) Cipher {
	// ctAlphabet := Backpermute(ptAlphabet, transform)

	pt2ct := make(map[rune]rune)
	ct2pt := make(map[rune]rune)

	ctRunes := []rune(ctAlphabet)

	for i, ptRune := range []rune(ptAlphabet) {
		ctRune := ctRunes[i]
		pt2ct[ptRune] = ctRune
		ct2pt[ctRune] = ptRune
	}

	return &simpleSubstitutionCipher{
		ptAlphabet: ptAlphabet,
		ctAlphabet: ctAlphabet,
		pt2ct:      pt2ct,
		ct2pt:      ct2pt,
		// Encipher: func(s string, strict bool) string {
		// 	return pt2ct.Transform(s, strict)
		// },
		// Decipher: func(s string, strict bool) string {
		// 	return ct2pt.Transform(s, strict)
		// },
	}
}

func (c *simpleSubstitutionCipher) String() string {
	return fmt.Sprintf("PT: %s\nCT: %s", c.ptAlphabet, c.ctAlphabet)
}

// Encipher a message from plaintext to ciphertext.
func (c *simpleSubstitutionCipher) Encipher(s string, strict bool) string {
	var out strings.Builder
	for _, r := range s {
		if o, found := c.encipherRune(r); found || !strict {
			out.WriteRune(o)
		}
	}
	return out.String()
}

// Decipher a message from ciphertext to plaintext.
func (c *simpleSubstitutionCipher) Decipher(s string, strict bool) string {
	var out strings.Builder
	for _, r := range s {
		if o, found := c.decipherRune(r); found || !strict {
			out.WriteRune(o)
		}
	}
	return out.String()
}

// EncipherRune transforms a rune from plaintext to ciphertext, returning it unchanged if transformation fails.
func (c *simpleSubstitutionCipher) encipherRune(r rune) (rune, bool) {
	if o, ok := c.pt2ct[r]; ok {
		return o, ok
	}
	return r, false
}

// DecipherRune transforms a rune from ciphertext to plaintext, returning it unchanged if transformation fails.
func (c *simpleSubstitutionCipher) decipherRune(r rune) (rune, bool) {
	if o, ok := c.ct2pt[r]; ok {
		return o, ok
	}
	return r, false
}

// NewKeywordCipher creates a new keyword cipher.
func NewKeywordCipher(alphabet, keyword string) Cipher {
	ctAlphabet := deduplicateString(keyword + alphabet)
	return NewSimpleSubstitutionCipher(alphabet, ctAlphabet)
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

	return NewSimpleSubstitutionCipher(ptAlphabet, ctAlphabet)
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
