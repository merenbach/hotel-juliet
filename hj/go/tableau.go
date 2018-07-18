package main

import (
	"fmt"
	"strings"
)

// A Cipher interfaces a data structure than can encipher and decipher strings.
// TODO: should `strict` be in creation, not Encipherion/Decipherion?
type Cipher interface {
	String() string
	Encipher(string, bool) string
	Decipher(string, bool) string
}

// A SimpleTableau represents a simple monoalphabetic substitution cipher
// PROBLEM WITH THIS MODEL: we need two functions, one for decryption
// WE CAN USE the invert/backpermute concept to map numbers...
// or just use a table directly and find a way to permute in the constructor??
// then we can still do all the work here (MakeTableau).
type SimpleTableau struct {
	ptAlphabet string
	ctAlphabet string

	pt2ct map[rune]rune
	ct2pt map[rune]rune
}

// NewSimpleTableau creates a reciprocal, monoalphabetic substitution cipher.
func NewSimpleTableau(ptAlphabet string, ctAlphabet string) Cipher {
	// ctAlphabet := Backpermute(ptAlphabet, transform)

	pt2ct := make(map[rune]rune)
	ct2pt := make(map[rune]rune)

	ctRunes := []rune(ctAlphabet)

	for i, ptRune := range []rune(ptAlphabet) {
		ctRune := ctRunes[i]
		pt2ct[ptRune] = ctRune
		ct2pt[ctRune] = ptRune
	}

	return &SimpleTableau{
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

// func (t *SimpleTableau) Plaintext() string {
// 	return t.ptAlphabet

// }
// func (t *SimpleTableau) Ciphertext() string {
// 	return t.ctAlphabet
// }

func (t *SimpleTableau) String() string {
	return fmt.Sprintf("PT: %s\nCT: %s", t.ptAlphabet, t.ctAlphabet)
}

// [TODO] Maybe these should be methods on a Message struct, as we explored before, for ease of chaining.

// Encipher a message from plaintext to ciphertext.
func (t *SimpleTableau) Encipher(s string, strict bool) string {
	var out strings.Builder
	for _, r := range s {
		o, found := t.encipherRune(r)
		if found || !strict {
			out.WriteRune(o)
		}
	}
	return out.String()
}

// Decipher a message from ciphertext to plaintext.
func (t *SimpleTableau) Decipher(s string, strict bool) string {
	var out strings.Builder
	for _, r := range s {
		o, found := t.decipherRune(r)
		if found || !strict {
			out.WriteRune(o)
		}
	}
	return out.String()
}

// EncipherRune transforms a rune from plaintext to ciphertext, returning it unchanged if transformation fails.
func (t *SimpleTableau) encipherRune(r rune) (rune, bool) {
	if o, ok := t.pt2ct[r]; ok {
		return o, ok
	}
	return r, false
}

// DecipherRune transforms a rune from ciphertext to plaintext, returning it unchanged if transformation fails.
func (t *SimpleTableau) decipherRune(r rune) (rune, bool) {
	if o, ok := t.ct2pt[r]; ok {
		return o, ok
	}
	return r, false
}

// // Simple monoalphabetic substitution cipher
// type tableau struct {
// 	ptAlphabet string
// 	ctAlphabet string
// }

// func (t tableau) String() string {
// 	return fmt.Sprintf("PT: %s\nCT: %s", t.ptAlphabet, t.ctAlphabet)
// }

// // Pt2Ct returns a closure to transform a string
// func (t tableau) Pt2Ct() func(string) string {
// 	xtable := ziprunes([]rune(t.ptAlphabet), []rune(t.ctAlphabet))
// 	return mapRuneTransform(xtable)
// }

// // Ct2Pt returns a closure to transform a string
// func (t tableau) Ct2Pt() func(string) string {
// 	xtable := ziprunes([]rune(t.ctAlphabet), []rune(t.ptAlphabet))
// 	return mapRuneTransform(xtable)
// }
