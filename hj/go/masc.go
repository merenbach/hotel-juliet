package main

// Monoalphabetic substitution ciphers

import (
	"fmt"
	"strings"
	"unicode/utf8"
)

// A SimpleSubstitutionCipher represents a simple monoalphabetic substitution cipher.
type SimpleSubstitutionCipher struct {
	ptAlphabet string
	ctAlphabet string

	pt2ct map[rune]rune
	ct2pt map[rune]rune
}

// NewSimpleSubstitutionCipher creates a reciprocal, monoalphabetic substitution cipher.
func NewSimpleSubstitutionCipher(ptAlphabet string, ctAlphabet string) *SimpleSubstitutionCipher {
	// ctAlphabet := Backpermute(ptAlphabet, transform)

	pt2ct := make(map[rune]rune)
	ct2pt := make(map[rune]rune)

	ctRunes := []rune(ctAlphabet)

	for i, ptRune := range []rune(ptAlphabet) {
		ctRune := ctRunes[i]
		pt2ct[ptRune] = ctRune
		ct2pt[ctRune] = ptRune
	}

	return &SimpleSubstitutionCipher{
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

func (c *SimpleSubstitutionCipher) String() string {
	return fmt.Sprintf("PT: %s\nCT: %s", c.ptAlphabet, c.ctAlphabet)
}

// Encipher a message from plaintext to ciphertext.
func (c *SimpleSubstitutionCipher) Encipher(s string, strict bool) string {
	var out strings.Builder
	for _, r := range s {
		if o, found := c.encipherRune(r); found || !strict {
			out.WriteRune(o)
		}
	}
	return out.String()
}

// Decipher a message from ciphertext to plaintext.
func (c *SimpleSubstitutionCipher) Decipher(s string, strict bool) string {
	var out strings.Builder
	for _, r := range s {
		if o, found := c.decipherRune(r); found || !strict {
			out.WriteRune(o)
		}
	}
	return out.String()
}

// EncipherRune transforms a rune from plaintext to ciphertext, returning it unchanged if transformation fails.
func (c *SimpleSubstitutionCipher) encipherRune(r rune) (rune, bool) {
	if o, ok := c.pt2ct[r]; ok {
		return o, ok
	}
	return r, false
}

// DecipherRune transforms a rune from ciphertext to plaintext, returning it unchanged if transformation fails.
func (c *SimpleSubstitutionCipher) decipherRune(r rune) (rune, bool) {
	if o, ok := c.ct2pt[r]; ok {
		return o, ok
	}
	return r, false
}

// NewKeywordCipher creates a new keyword cipher.
func NewKeywordCipher(alphabet, keyword string) *SimpleSubstitutionCipher {
	ctAlphabet := deduplicate(keyword + alphabet)
	return NewSimpleSubstitutionCipher(alphabet, ctAlphabet)
}

// NewAffineCipher creates a new affine cipher.
func NewAffineCipher(ptAlphabet string, a, b int) *SimpleSubstitutionCipher {
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
func NewAtbashCipher(ptAlphabet string) *SimpleSubstitutionCipher {
	return NewAffineCipher(ptAlphabet, -1, -1)
}

// NewCaesarCipher creates a new Caesar cipher.
func NewCaesarCipher(ptAlphabet string, b int) *SimpleSubstitutionCipher {
	return NewAffineCipher(ptAlphabet, 1, b)
}

// NewDecimationCipher creates a new decimation cipher.
func NewDecimationCipher(ptAlphabet string, a int) *SimpleSubstitutionCipher {
	return NewAffineCipher(ptAlphabet, a, 0)
}

// NewRot13Cipher creates a new Rot13 (Caesar shift of 13) cipher.
func NewRot13Cipher(ptAlphabet string) *SimpleSubstitutionCipher {
	return NewCaesarCipher(ptAlphabet, 13)
}
