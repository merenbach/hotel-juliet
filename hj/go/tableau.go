package main

import (
	"fmt"
	"strings"
)

// Tableau represents a simple monoalphabetic substitution cipher
type Tableau struct {
	Alphabet string
	Pt2Ct    map[rune]rune
	Ct2Pt    map[rune]rune
}

func (t Tableau) String() string {
	var (
		pt strings.Builder
		ct strings.Builder
	)

	pt.WriteString("PT: ")
	ct.WriteString("CT: ")
	for _, a := range []rune(t.Alphabet) {
		pt.WriteRune(a)
		ct.WriteRune(t.Pt2Ct[a])
	}
	return pt.String() + "\n" + ct.String()
}

// MakeTableau creates a tableau based on the given plaintext alphabet and transform function.
func MakeTableau(ptAlphabet string, transform func(int) int) Tableau {
	ctAlphabet := Backpermute(ptAlphabet, transform)

	t := Tableau{
		Alphabet: ptAlphabet,
		Pt2Ct:    ziprunes([]rune(ptAlphabet), []rune(ctAlphabet)),
		Ct2Pt:    ziprunes([]rune(ctAlphabet), []rune(ptAlphabet)),
	}
	return t
}

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
