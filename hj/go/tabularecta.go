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
	countersign   string
	Textautoclave bool
	Keyautoclave  bool
}

func (tr *TabulaRecta) String() string {
	var out strings.Builder
	formatForPrinting := func(s string) string {
		spl := strings.Split(s, "")
		return strings.Join(spl, " ")
	}
	out.WriteString("    " + formatForPrinting(tr.ptAlphabet) + "\n  +")
	for _ = range []rune(tr.ptAlphabet) {
		out.WriteRune('-')
		out.WriteRune('-')
	}
	for _, r := range []rune(tr.keyAlphabet) {
		c := tr.keysToCiphers[r]
		ctAlpha := fmt.Sprintf("\n%c | %s", r, formatForPrinting(c.(*SimpleTableau).ctAlphabet))
		out.WriteString(ctAlpha)
	}
	return out.String()
}

// NOTE: we roll the countersign into the tabula recta so it has all the data it needs
// to decode/encode a string reusably, for parallelism with the monoalphabetic ciphers.
func NewTabulaRecta(countersign, ptAlphabet, ctAlphabet, keyAlphabet string) Cipher {
	tr := TabulaRecta{
		ptAlphabet:    ptAlphabet,
		ctAlphabet:    ctAlphabet,
		tableaux:      make([]Cipher, 0),
		keyAlphabet:   keyAlphabet,
		countersign:   countersign,
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

func (tr *TabulaRecta) Encipher(s string, strict bool) string {
	var out strings.Builder
	kRunes := []rune(tr.countersign)
	var transcodedCharCount = 0
	for _, r := range []rune(s) {
		k := kRunes[transcodedCharCount%len(kRunes)]
		cipher := tr.keysToCiphers[k]
		o := cipher.Encipher(string(r), true)
		if o != "" {
			out.WriteRune([]rune(o)[0])
			transcodedCharCount++

			if tr.Textautoclave {
				kRunes = append(kRunes, r)
			} else if tr.Keyautoclave {
				kRunes = append(kRunes, []rune(o)...)
			}
		} else if !strict {
			out.WriteRune(r)
		}
	}
	return out.String()
}

func (tr *TabulaRecta) Decipher(s string, strict bool) string {
	var out strings.Builder
	kRunes := []rune(tr.countersign)
	var transcodedCharCount = 0
	for _, r := range []rune(s) {
		k := kRunes[transcodedCharCount%len(kRunes)]
		cipher := tr.keysToCiphers[k]
		o := cipher.Decipher(string(r), true)
		if o != "" {
			out.WriteRune([]rune(o)[0])
			transcodedCharCount++
			if tr.Textautoclave {
				kRunes = append(kRunes, []rune(o)...)
			} else if tr.Keyautoclave {
				kRunes = append(kRunes, r)
			}
		} else if !strict {
			out.WriteRune(r)
		}
	}
	return out.String()
}

// WrapString wraps a string a specified number of indices.
// WrapString will error out if the provided offset is negative.
func wrapString(s string, i int) string {
	// if we simply `return s[i:] + s[:i]`, we're operating on bytes, not runes
	u := []rune(s)
	v := append(u[i:], u[:i]...)
	return string(v)
}
