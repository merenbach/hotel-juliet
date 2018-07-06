package main

import (
	"fmt"
	"strings"
)

// Tableau represents a simple monoalphabetic substitution cipher
// PROBLEM WITH THIS MODEL: we need two functions, one for decryption
// WE CAN USE the invert/backpermute concept to map numbers...
// or just use a table directly and find a way to permute in the constructor??
// then we can still do all the work here (MakeTableau).
type Tableau struct {
	ptAlphabet string
	ctAlphabet string

	f func(int) int

	pt2num map[rune]int
	num2pt map[int]rune

	ct2num map[rune]int
	num2ct map[int]rune
}

func (t Tableau) String() string {
	return fmt.Sprintf("PT: %s\nCT: %s", t.ptAlphabet, t.Pt2Ct(t.ptAlphabet))
}

// MakeTableau creates a tableau based on the given plaintext alphabet and transform function.
// If ctAlphabet is blank, it will be set to the ptAlphabet.
func MakeTableau(ptAlphabet string, ctAlphabet string, transform func(int) int) Tableau {
	if ctAlphabet == "" {
		ctAlphabet = ptAlphabet
	}

	// ctAlphabet := Backpermute(ptAlphabet, transform)

	pt2num := make(map[rune]int)
	num2pt := make(map[int]rune)
	for i, r := range []rune(ptAlphabet) {
		pt2num[r] = i
		num2pt[i] = r
	}

	ct2num := make(map[rune]int)
	num2ct := make(map[int]rune)
	for i, r := range []rune(ctAlphabet) {
		ct2num[r] = i
		num2ct[i] = r
	}

	t := Tableau{
		ptAlphabet: ptAlphabet,
		ctAlphabet: ctAlphabet,
		f:          transform,
		pt2num:     pt2num,
		num2pt:     num2pt,
		ct2num:     ct2num,
		num2ct:     num2ct,
	}
	return t
}

// Pt2Ct converts plaintext to ciphertext.
func (t Tableau) Pt2Ct(s string) string {
	var out strings.Builder
	for _, r := range []rune(s) {
		i := t.pt2num[r]
		o := t.f(i)
		r2 := t.num2ct[o]
		out.WriteRune(r2)
	}
	return out.String()
}

// Ct2Pt converts ciphertext to plaintext.
func (t Tableau) Ct2Pt(s string) string {
	var out strings.Builder
	for _, r := range []rune(s) {
		i := t.ct2num[r]
		o := t.f(i)
		r2 := t.num2pt[o]
		out.WriteRune(r2)
	}
	return out.String()
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
