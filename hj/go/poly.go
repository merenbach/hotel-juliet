package main

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

// // NewAffineCipher creates a new affine cipher.
// func NewAffineCipher(ptAlphabet string, a, b int) Cipher {
// 	m := utf8.RuneCountInString(ptAlphabet)

// 	// TODO: consider using Hull-Dobell satisfaction to determine if `a` is valid (must be coprime with `m`)
// 	for a < 0 {
// 		a += m
// 	}
// 	for b < 0 {
// 		b += m
// 	}

// 	lcg := NewLCG(uint(m), 1, uint(a), uint(b))
// 	ctAlphabet := Backpermute(ptAlphabet, lcg.Next)

// 	return NewSimpleTableau(ptAlphabet, ctAlphabet)
// }

// // NewAtbashCipher creates a new Atbash cipher.
// func NewAtbashCipher(ptAlphabet string) Cipher {
// 	return NewAffineCipher(ptAlphabet, -1, -1)
// }

// // NewCaesarCipher creates a new Caesar cipher.
// func NewCaesarCipher(ptAlphabet string, b int) Cipher {
// 	return NewAffineCipher(ptAlphabet, 1, b)
// }

// // NewDecimationCipher creates a new decimation cipher.
// func NewDecimationCipher(ptAlphabet string, a int) Cipher {
// 	return NewAffineCipher(ptAlphabet, a, 0)
// }

// // NewRot13Cipher creates a new Rot13 (Caesar shift of 13) cipher.
// func NewRot13Cipher(ptAlphabet string) Cipher {
// 	return NewCaesarCipher(ptAlphabet, 13)
// }
