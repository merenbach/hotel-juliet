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
	ciphers       map[rune]Cipher
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
	for range tr.ptAlphabet {
		out.WriteRune('-')
		out.WriteRune('-')
	}
	for _, r := range tr.keyAlphabet {
		c := tr.ciphers[r]
		ctAlpha := fmt.Sprintf("\n%c | %s", r, formatForPrinting(c.(*SimpleTableau).ctAlphabet))
		out.WriteString(ctAlpha)
	}
	return out.String()
}

// NewTabulaRecta creates a new tabula recta suitable for use with the Vigenere family of ciphers.
// NOTE: we roll the countersign into the tabula recta so it has all the data it needs
// to decode/encode a string reusably, for parallelism with the monoalphabetic ciphers.
func NewTabulaRecta(countersign, ptAlphabet, ctAlphabet, keyAlphabet string) Cipher {
	tr := TabulaRecta{
		ptAlphabet:  ptAlphabet,
		ctAlphabet:  ctAlphabet,
		keyAlphabet: keyAlphabet,
		countersign: countersign,
		ciphers:     make(map[rune]Cipher),
	}
	for i, r := range []rune(keyAlphabet) {
		ctAlphabet3 := wrapString(ctAlphabet, i)
		t := NewSimpleTableau(ptAlphabet, ctAlphabet3)
		// t := NewSimpleTableau(ptAlphabet, ctAlphabet3)
		tr.ciphers[r] = t
	}
	return &tr
}

// NewDellaPortaReciprocalTable creates a new tabula recta suitable for use with the Della Porta cipher.
func NewDellaPortaReciprocalTable(countersign, ptAlphabet, ctAlphabet, keyAlphabet string) Cipher {
	tr := TabulaRecta{
		ptAlphabet:  ptAlphabet,
		ctAlphabet:  ctAlphabet,
		keyAlphabet: keyAlphabet,
		countersign: countersign,
		ciphers:     make(map[rune]Cipher),
	}
	if len(ctAlphabet)%2 != 0 {
		panic("Della Porta cipher alphabets must have even length")
	}
	ctAlphabet2 := wrapString(ctAlphabet, len(ctAlphabet)/2)
	for i, r := range []rune(keyAlphabet) {
		ctAlphabet3 := owrapString(ctAlphabet2, i/2)
		t := NewSimpleTableau(ptAlphabet, ctAlphabet3)
		tr.ciphers[r] = t
	}
	return &tr
}

// Encipher a message from plaintext to ciphertext.
func (tr *TabulaRecta) Encipher(s string, strict bool) string {
	var out strings.Builder
	keyRunes := []rune(tr.countersign)
	var transcodedCharCount = 0
	for _, r := range s {
		k := keyRunes[transcodedCharCount%len(keyRunes)]
		cipher := tr.ciphers[k]
		if o, ok := cipher.(*SimpleTableau).encipherRune(r); ok {
			out.WriteRune(o)
			transcodedCharCount++

			if tr.Textautoclave {
				keyRunes = append(keyRunes, r)
			} else if tr.Keyautoclave {
				keyRunes = append(keyRunes, o)
			}
		} else if !strict {
			out.WriteRune(r)
		}
	}
	return out.String()
}

// Decipher a message from ciphertext to plaintext.
func (tr *TabulaRecta) Decipher(s string, strict bool) string {
	var out strings.Builder
	keyRunes := []rune(tr.countersign)
	var transcodedCharCount = 0
	for _, r := range s {
		k := keyRunes[transcodedCharCount%len(keyRunes)]
		cipher := tr.ciphers[k]
		if o, ok := cipher.(*SimpleTableau).decipherRune(r); ok {
			out.WriteRune(o)
			transcodedCharCount++
			if tr.Textautoclave {
				keyRunes = append(keyRunes, o)
			} else if tr.Keyautoclave {
				keyRunes = append(keyRunes, r)
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
	rr := []rune(s)
	return string(rr[i:]) + string(rr[:i])
}

// WrapString wraps a string a specified number of indices.
// WrapString will error out if the provided offset is negative.
func owrapString(s string, i int) string {
	// if we simply `return s[i:] + s[:i]`, we're operating on bytes, not runes
	if len([]rune(s))%2 != 0 {
		panic("owrapString sequence length must be divisible by two")
	}
	sRunes := []rune(s)
	u, v := sRunes[:len(sRunes)/2], sRunes[len(sRunes)/2:]
	return wrapString(string(u), i) + wrapString(string(v), len(v)-i)
}
