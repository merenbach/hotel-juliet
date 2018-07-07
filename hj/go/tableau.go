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
		if !found && !strict {
			o = r
		}
		out.WriteRune(o)
	}
	return out.String()
}

// Tableau represents a simple monoalphabetic substitution cipher
// PROBLEM WITH THIS MODEL: we need two functions, one for decryption
// WE CAN USE the invert/backpermute concept to map numbers...
// or just use a table directly and find a way to permute in the constructor??
// then we can still do all the work here (MakeTableau).
type Tableau struct {
	ptAlphabet string
	ctAlphabet string

	Encrypt func(string, bool) string
	Decrypt func(string, bool) string
}

func (t Tableau) String() string {
	return fmt.Sprintf("PT: %s\nCT: %s", t.ptAlphabet, t.ctAlphabet)
}

// MakeTableau creates a tableau based on the given plaintext alphabet and transform function.
// If ctAlphabet is blank, it will be set to the ptAlphabet.
func MakeTableau(ptAlphabet string, ctAlphabet string) Tableau {
	if ctAlphabet == "" {
		ctAlphabet = ptAlphabet
	}

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

	t := Tableau{
		ptAlphabet: ptAlphabet,
		ctAlphabet: ctAlphabet,
		Encrypt: func(s string, strict bool) string {
			return pt2ct.Transform(s, strict)
		},
		Decrypt: func(s string, strict bool) string {
			return ct2pt.Transform(s, strict)
		},
	}
	return t
}

// [TODO] Maybe these should be methods on a Message struct, as we explored before, for ease of chaining.

// // Pt2Ct converts plaintext to ciphertext.
// func (t Tableau) Encrypt(s string, strict bool) string {
// 	return t.pt2ct(s, strict)
// }

// // Ct2Pt converts ciphertext to plaintext.
// func (t Tableau) Decrypt(s string, strict bool) string {
// 	return t.ct2pt(s, strict)
// }

// Simple monoalphabetic substitution cipher
type tableau struct {
	ptAlphabet string
	ctAlphabet string
}

func (t tableau) String() string {
	return fmt.Sprintf("PT: %s\nCT: %s", t.ptAlphabet, t.ctAlphabet)
}

// Pt2Ct returns a closure to transform a string
func (t tableau) Pt2Ct() func(string) string {
	xtable := ziprunes([]rune(t.ptAlphabet), []rune(t.ctAlphabet))
	return mapRuneTransform(xtable)
}

// Ct2Pt returns a closure to transform a string
func (t tableau) Ct2Pt() func(string) string {
	xtable := ziprunes([]rune(t.ctAlphabet), []rune(t.ptAlphabet))
	return mapRuneTransform(xtable)
}
