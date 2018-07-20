package main

import (
	"fmt"
	"sort"
	"strings"
)

// Polyalphabetic substitution ciphers

// TabulaRecta holds a tabula recta.
type tabulaRecta struct {
	ptAlphabet    string
	ctAlphabet    string
	keyAlphabet   string
	ciphers       map[rune]Cipher
	countersign   string
	Textautoclave bool
	Keyautoclave  bool
}

func (tr *tabulaRecta) String() string {
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
		ctAlpha := fmt.Sprintf("\n%c | %s", r, formatForPrinting(c.(*simpleSubstitutionCipher).ctAlphabet))
		out.WriteString(ctAlpha)
	}
	return out.String()
}

// NewTabulaRecta creates a new tabula recta suitable for use with the Vigenere family of ciphers.
// NOTE: we roll the countersign into the tabula recta so it has all the data it needs
// to decode/encode a string reusably, for parallelism with the monoalphabetic ciphers.
func NewTabulaRecta(countersign, ptAlphabet, ctAlphabet, keyAlphabet string) Cipher {
	tr := tabulaRecta{
		ptAlphabet:  ptAlphabet,
		ctAlphabet:  ctAlphabet,
		keyAlphabet: keyAlphabet,
		countersign: countersign,
		ciphers:     make(map[rune]Cipher),
	}
	// this cast is necessary to ensure that the index increases without gaps
	for i, r := range []rune(keyAlphabet) {
		ctAlphabet3 := wrapString(ctAlphabet, i)
		tr.ciphers[r] = NewSimpleSubstitutionCipher(ptAlphabet, ctAlphabet3)
	}
	return &tr
}

// NewDellaPortaReciprocalTable creates a new tabula recta suitable for use with the Della Porta cipher.
func NewDellaPortaReciprocalTable(countersign, ptAlphabet, ctAlphabet, keyAlphabet string) Cipher {
	tr := tabulaRecta{
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
	// this cast is necessary to ensure that the index increases without gaps
	for i, r := range []rune(keyAlphabet) {
		ctAlphabet3 := owrapString(ctAlphabet2, i/2)
		tr.ciphers[r] = NewSimpleSubstitutionCipher(ptAlphabet, ctAlphabet3)
	}
	return &tr
}

// Encipher a message from plaintext to ciphertext.
func (tr *tabulaRecta) Encipher(s string, strict bool) string {
	var out strings.Builder
	keyRunes := []rune(tr.countersign)
	var transcodedCharCount = 0
	for _, r := range s {
		k := keyRunes[transcodedCharCount%len(keyRunes)]
		cipher := tr.ciphers[k]
		if o, ok := cipher.(*simpleSubstitutionCipher).encipherRune(r); ok {
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
func (tr *tabulaRecta) Decipher(s string, strict bool) string {
	var out strings.Builder
	keyRunes := []rune(tr.countersign)
	var transcodedCharCount = 0
	for _, r := range s {
		k := keyRunes[transcodedCharCount%len(keyRunes)]
		cipher := tr.ciphers[k]
		if o, ok := cipher.(*simpleSubstitutionCipher).decipherRune(r); ok {
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

// NewVigenereCipher creates a new Vigenere cipher.
func NewVigenereCipher(countersign, alphabet string) Cipher {
	return NewTabulaRecta(countersign, alphabet, alphabet, alphabet)
}

// NewVigenereTextAutoclaveCipher creates a new Vigenere (text autoclave) cipher.
func NewVigenereTextAutoclaveCipher(countersign, alphabet string) Cipher {
	c := NewTabulaRecta(countersign, alphabet, alphabet, alphabet)
	c.(*tabulaRecta).Textautoclave = true
	return c
}

// NewVigenereKeyAutoclaveCipher creates a new Vigenere (key autoclave) cipher.
func NewVigenereKeyAutoclaveCipher(countersign, alphabet string) Cipher {
	c := NewTabulaRecta(countersign, alphabet, alphabet, alphabet)
	c.(*tabulaRecta).Keyautoclave = true
	return c
}

// NewBeaufortCipher creates a new Beaufort cipher.
func NewBeaufortCipher(countersign, alphabet string) Cipher {
	revAlphabet := reverseString(alphabet)
	return NewTabulaRecta(countersign, alphabet, revAlphabet, revAlphabet)
}

// NewGronsfeldCipher creates a new Gronsfeld cipher.
func NewGronsfeldCipher(countersign, alphabet string) Cipher {
	return NewTabulaRecta(countersign, alphabet, alphabet, "0123456789")
}

// NewVariantBeaufortCipher creates a new Vigenere cipher.
func NewVariantBeaufortCipher(countersign, alphabet string) Cipher {
	revAlphabet := reverseString(alphabet)
	return NewTabulaRecta(countersign, revAlphabet, revAlphabet, alphabet)
}

// NewTrithemiusCipher creates a new Trithemius cipher.
// NewTrithemiusCipher considers this simply the Vigenere cipher with the countersign equal to the alphabet.
func NewTrithemiusCipher(alphabet string) Cipher {
	countersign := alphabet
	return NewVigenereCipher(countersign, alphabet)
}

// NewDellaPortaCipher creates a new DellaPorta cipher.
func NewDellaPortaCipher(countersign, alphabet string) Cipher {
	return NewDellaPortaReciprocalTable(countersign, alphabet, alphabet, alphabet)
}

// ReverseString reverses the runes in a string.
func reverseString(s string) string {
	r := []rune(s)
	sort.SliceStable(r, func(i, j int) bool {
		return true
	})
	return string(r)
}
