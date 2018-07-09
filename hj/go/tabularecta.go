package main

import (
	"fmt"
	"strings"
)

// TabulaRecta holds a tabula recta.
type TabulaRecta struct {
	ptAlphabet    string
	ctAlphabet    string
	keyAlphabet   string
	tableaux      []Cipher
	keysToCiphers map[rune]Cipher
}

func (tr *TabulaRecta) String() string {
	out := make([]string, 0)
	formatForPrinting := func(s string) string {
		spl := strings.Split(s, "")
		return strings.Join(spl, " ")
	}
	out = append(out, "    "+formatForPrinting(tr.ptAlphabet))
	out = append(out, "-----")
	for _, r := range []rune(tr.keyAlphabet) {
		c := tr.keysToCiphers[r]
		ctAlpha := fmt.Sprintf("%c | %s", r, formatForPrinting(c.(*SimpleTableau).ctAlphabet))
		out = append(out, ctAlpha)
	}
	return strings.Join(out, "\n")
}

func NewTabulaRecta(ptAlphabet, ctAlphabet string, keyAlphabet string) *TabulaRecta {
	tr := TabulaRecta{
		ptAlphabet:    ptAlphabet,
		ctAlphabet:    ctAlphabet,
		tableaux:      make([]Cipher, 0),
		keyAlphabet:   keyAlphabet,
		keysToCiphers: make(map[rune]Cipher),
	}
	for i, r := range []rune(keyAlphabet) {
		ctAlphabet_ := wrapString(ctAlphabet, i)
		t := NewSimpleTableau(ptAlphabet, ctAlphabet_)
		tr.tableaux = append(tr.tableaux, t)
		tr.keysToCiphers[r] = t
	}
	return &tr
}

func (tr *TabulaRecta) Encrypt(s, key string, strict bool) string {
	var out strings.Builder
	kRunes := []rune(key)
	var transcodedCharCount = 0
	for _, r := range []rune(s) {
		k := kRunes[transcodedCharCount%len(key)]
		cipher := tr.keysToCiphers[k]
		o := cipher.Encrypt(string(r), true)
		if o != "" {
			out.WriteRune([]rune(o)[0])
			transcodedCharCount++
		} else if !strict {
			out.WriteRune(r)
		}
	}
	return out.String()
}

func (tr *TabulaRecta) Decrypt(s, key string, strict bool) string {
	var out strings.Builder
	kRunes := []rune(key)
	var transcodedCharCount = 0
	for _, r := range []rune(s) {
		k := kRunes[transcodedCharCount%len(key)]
		cipher := tr.keysToCiphers[k]
		o := cipher.Decrypt(string(r), true)
		if o != "" {
			out.WriteRune([]rune(o)[0])
			transcodedCharCount++
		} else if !strict {
			out.WriteRune(r)
		}
	}
	return out.String()
}
