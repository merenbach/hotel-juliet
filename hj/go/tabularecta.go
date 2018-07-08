package main

import (
	"fmt"
	"strings"
)

// TabulaRecta holds a tabula recta.
type TabulaRecta struct {
	ptAlphabet    string
	keys          string
	tableaux      []Cipher
	keysToCiphers map[rune]Cipher
}

func (tr *TabulaRecta) String() string {
	out := make([]string, 0)
	formatForPrinting := func(s string) string {
		spl := strings.Split(s, "")
		return strings.Join(spl, " ")
	}
	out = append(out, formatForPrinting(tr.ptAlphabet))
	out = append(out, "-----")
	// for _, t := range tr.tableaux {
	// 	out = append(out, formatForPrinting(t.(*SimpleTableau).Ciphertext()))
	// }
	return strings.Join(out, "\n")
}

func NewTabulaRecta(ptAlphabet, ctAlphabet string, key string) *TabulaRecta {
	tr := TabulaRecta{
		ptAlphabet:    ptAlphabet,
		tableaux:      make([]Cipher, 0),
		keysToCiphers: make(map[rune]Cipher),
	}
	for i, r := range []rune(key) {
		t := NewCaesarCipher(ctAlphabet, i)
		tr.tableaux = append(tr.tableaux, t)
		tr.keysToCiphers[r] = t
	}
	tr.keys = key
	return &tr
}

func (tr *TabulaRecta) Encrypt(s, key string, strict bool) string {
	var out strings.Builder
	kRunes := []rune(key)
	var transcodedCharCount = 0
	for _, r := range []rune(s) {
		k := kRunes[transcodedCharCount%len(key)]
		cipher := tr.keysToCiphers[k]
		fmt.Println("r string = ", string(r))
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
