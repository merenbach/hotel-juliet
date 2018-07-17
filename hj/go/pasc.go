package main

import "sort"

// Monoalphabetic substitution ciphers

// NewVigenereCipher creates a new Vigenere cipher.
func NewVigenereCipher(countersign, alphabet string) Cipher {
	return NewTabulaRecta(countersign, alphabet, alphabet, alphabet)
}

// NewVigenereTextAutoclaveCipher creates a new Vigenere (text autoclave) cipher.
func NewVigenereTextAutoclaveCipher(countersign, alphabet string) Cipher {
	c := NewTabulaRecta(countersign, alphabet, alphabet, alphabet)
	c.(*TabulaRecta).Textautoclave = true
	return c
}

// NewVigenereKeyAutoclaveCipher creates a new Vigenere (key autoclave) cipher.
func NewVigenereKeyAutoclaveCipher(countersign, alphabet string) Cipher {
	c := NewTabulaRecta(countersign, alphabet, alphabet, alphabet)
	c.(*TabulaRecta).Keyautoclave = true
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

// // NewDellaPortaCipher creates a new DellaPorta cipher.
// func NewDellaPortaCipher(alphabet string) Cipher {
// 	return NewTabulaRecta(alphabet, alphabet, "0123456789")
// }

// ReverseString reverses the runes in a string.
func reverseString(s string) string {
	r := []rune(s)
	sort.SliceStable(r, func(i, j int) bool {
		return true
	})
	return string(r)
}
