package main

import (
	"fmt"
	"strings"
)

type RuneMap map[rune]rune

// Transform a string based on a rune-to-rune mapping.
func (m *RuneMap) Transform(s string, strict bool) string {
	var out strings.Builder
	for _, r := range []rune(s) {
		o, found := (*m)[r]
		if found {
			out.WriteRune(o)
		} else if !strict {
			out.WriteRune(r)
		}
	}
	return out.String()
}

// TODO: should `strict` be in creation, not Encryption/Decryption?
type Cipher interface {
	String() string
	Encrypt(string, bool) string
	Decrypt(string, bool) string
}

// Tableau represents a simple monoalphabetic substitution cipher
// PROBLEM WITH THIS MODEL: we need two functions, one for decryption
// WE CAN USE the invert/backpermute concept to map numbers...
// or just use a table directly and find a way to permute in the constructor??
// then we can still do all the work here (MakeTableau).
type SimpleTableau struct {
	ptAlphabet string
	ctAlphabet string

	pt2ct *RuneMap
	ct2pt *RuneMap
}

// NewTableau creates a reciprocal, monoalphabetic substitution cipher.
func NewSimpleTableau(ptAlphabet string, ctAlphabet string) Cipher {
	// ctAlphabet := Backpermute(ptAlphabet, transform)

	// pt2ct := make(map[rune]rune)
	// ct2pt := make(map[rune]rune)
	pt2ct := make(RuneMap)
	ct2pt := make(RuneMap)

	ptRunes := []rune(ptAlphabet)
	ctRunes := []rune(ctAlphabet)

	for i := range []rune(ptAlphabet) {
		ptRune := ptRunes[i]
		ctRune := ctRunes[i]
		pt2ct[ptRune] = ctRune
		ct2pt[ctRune] = ptRune
	}

	return &SimpleTableau{
		ptAlphabet: ptAlphabet,
		ctAlphabet: ctAlphabet,
		pt2ct:      &pt2ct,
		ct2pt:      &ct2pt,
		// Encrypt: func(s string, strict bool) string {
		// 	return pt2ct.Transform(s, strict)
		// },
		// Decrypt: func(s string, strict bool) string {
		// 	return ct2pt.Transform(s, strict)
		// },
	}
}

func (t *SimpleTableau) String() string {
	return fmt.Sprintf("PT: %s\nCT: %s", t.ptAlphabet, t.ctAlphabet)
}

// [TODO] Maybe these should be methods on a Message struct, as we explored before, for ease of chaining.

// Encrypt a message from plaintext to ciphertext.
func (t *SimpleTableau) Encrypt(s string, strict bool) string {
	return t.pt2ct.Transform(s, strict)
}

// Decrypt a message from ciphertext to plaintext.
func (t *SimpleTableau) Decrypt(s string, strict bool) string {
	return t.ct2pt.Transform(s, strict)
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
