package main

import "fmt"

// Simple monoalphabetic substitution cipher
type tableau struct {
	ptAlphabet string
	ctAlphabet string
}

func MakeTableau(ptAlphabet, ctAlphabet string) tableau {
	return tableau{ptAlphabet, ctAlphabet}
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
