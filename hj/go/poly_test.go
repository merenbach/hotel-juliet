package main

import "testing"

const defaultPolyalphabeticAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runPolyalphabeticReciprocalTests(t *testing.T, plaintext, ciphertext string, c Cipher, strict bool) {
	encrypted := c.Encrypt(plaintext, strict)
	decrypted := c.Decrypt(ciphertext, strict)
	if string(encrypted) != ciphertext {
		t.Errorf("ciphertext %q was incorrect; wanted %q", encrypted, ciphertext)
	}
	if string(decrypted) != plaintext {
		t.Errorf("plaintext %q was incorrect; wanted: %q", decrypted, plaintext)
	}
}

// TestVigenereCipher tests the keyword cipher.
func TestVigenereCipher(t *testing.T) {
	tables := []struct {
		alphabet    string
		plaintext   string
		ciphertext  string
		countersign string
		strict      bool
	}{
		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "VGPLB, KUILS!", "OCEANOGRAPHYWHAT", false},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO", false},
		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "CRHHLWLQHG", "KANGROOO", true},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLOWORLD", "KANGAROO", true},
	}
	for _, table := range tables {
		c := NewVigenereCipher(table.countersign, table.alphabet)
		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestBeaufortCipher tests the keyword cipher.
func TestBeaufortCipher(t *testing.T) {
	tables := []struct {
		alphabet    string
		plaintext   string
		ciphertext  string
		countersign string
		strict      bool
	}{
		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "HYTPZ, SSAPM!", "OCEANOGRAPHYWHAT", false},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO", false},
		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "CRHHLWLQHG", "KANGROOO", true},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLOWORLD", "KANGAROO", true},
	}
	for _, table := range tables {
		c := NewBeaufortCipher(table.countersign, table.alphabet)
		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestGronsfeldCipher tests the keyword cipher.
func TestGronsfeldCipher(t *testing.T) {
	tables := []struct {
		alphabet    string
		plaintext   string
		ciphertext  string
		countersign string
		strict      bool
	}{
		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "JHMOQ, YRSOF!", "23132", false},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO", false},
		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "CRHHLWLQHG", "KANGROOO", true},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLOWORLD", "KANGAROO", true},
	}
	for _, table := range tables {
		c := NewGronsfeldCipher(table.countersign, table.alphabet)
		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestTrithemiusCipher tests the keyword cipher.
func TestTrithemiusCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		strict     bool
	}{
		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "HFNOS, BUYTM!", false},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO", false},
		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "CRHHLWLQHG", "KANGROOO", true},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLOWORLD", "KANGAROO", true},
	}
	for _, table := range tables {
		c := NewTrithemiusCipher(table.alphabet)
		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestVariantBeaufortCipher tests the keyword cipher.
func TestVariantBeaufortCipher(t *testing.T) {
	tables := []struct {
		alphabet    string
		plaintext   string
		ciphertext  string
		countersign string
		strict      bool
	}{
		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "TCHLB, IIALO!", "OCEANOGRAPHYWHAT", false},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO", false},
		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "CRHHLWLQHG", "KANGROOO", true},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLOWORLD", "KANGAROO", true},
	}
	for _, table := range tables {
		c := NewVariantBeaufortCipher(table.countersign, table.alphabet)
		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// // TestAffineCipher tests the affine cipher.
// func TestAffineCipher(t *testing.T) {
// 	tables := []struct {
// 		alphabet   string
// 		plaintext  string
// 		ciphertext string
// 		a          int
// 		b          int
// 		strict     bool
// 	}{
// 		// {defaultPolyalphabeticAlphabet, "VGPLB, KUILS!", "HELLO, WORLD!", "OCEANOGRAPHYWHAT", false},
// 		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "VGPLB, KUILS!", "OCEANOGRAPHYWHAT", false},
// 		// {defaultPolyalphabeticAlphabet, "VGPLB, KUILS!", "HELLO, WORLD!", "OCEANOGRAPHYWHAT", false},
// 		// self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, IIALO!', block=None)
// 	}
// 	for _, table := range tables {
// 		c := NewVigenereCipher(table.alphabet, table.a, table.b)
// 		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)

// 	}
// }

// // TestAtbashCipher tests the Atbash cipher.
// func TestAtbashCipher(t *testing.T) {
// 	tables := []struct {
// 		alphabet   string
// 		plaintext  string
// 		ciphertext string
// 		strict     bool
// 	}{
// 		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "SVOOL, DLIOW!", false},
// 		{defaultPolyalphabeticAlphabet, "SVOOL, DLIOW!", "HELLO, WORLD!", false},
// 		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "SVOOLDLIOW", true},
// 		// {defaultPolyalphabeticAlphabet, "SVOOL, DLIOW!", "HELLOWORLD", true},
// 	}
// 	for _, table := range tables {
// 		c := NewAtbashCipher(table.alphabet)
// 		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
// 	}
// }

// // TestCaesarCipher tests the Caesar cipher.
// func TestCaesarCipher(t *testing.T) {
// 	tables := []struct {
// 		alphabet   string
// 		plaintext  string
// 		ciphertext string
// 		b          int
// 		strict     bool
// 	}{
// 		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "KHOOR, ZRUOG!", 3, false},
// 		{defaultPolyalphabeticAlphabet, "EBIIL, TLOIA!", "HELLO, WORLD!", 3, false},
// 		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "YVCCF, NFICU!", 17, false},
// 		{defaultPolyalphabeticAlphabet, "QNUUX, FXAUM!", "HELLO, WORLD!", 17, false},
// 		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "KHOORZRUOG", 3, true},
// 		// {defaultPolyalphabeticAlphabet, "EBIIL, TLOIA!", "HELLOWORLD", 3, true},
// 		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "YVCCFNFICU", 17, true},
// 		// {defaultPolyalphabeticAlphabet, "QNUUX, FXAUM!", "HELLOWORLD", 17, true},
// 	}
// 	for _, table := range tables {
// 		c := NewCaesarCipher(table.alphabet, table.b)
// 		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
// 	}
// }

// // TestDecimationCipher tests the decimation cipher.
// func TestDecimationCipher(t *testing.T) {
// 	tables := []struct {
// 		alphabet   string
// 		plaintext  string
// 		ciphertext string
// 		a          int
// 		strict     bool
// 	}{
// 		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "XCZZU, YUPZV!", 7, false},
// 		{defaultPolyalphabeticAlphabet, "BIJJC, SCVJT!", "HELLO, WORLD!", 7, false},
// 		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "XCZZUYUPZV", 7, true},
// 		// {defaultPolyalphabeticAlphabet, "BIJJC, SCVJT!", "HELLOWORLD", 7, true},
// 	}
// 	for _, table := range tables {
// 		c := NewDecimationCipher(table.alphabet, table.a)
// 		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
// 	}
// }

// // TestRot13Cipher tests the Rot13 cipher.
// func TestRot13Cipher(t *testing.T) {
// 	tables := []struct {
// 		alphabet   string
// 		plaintext  string
// 		ciphertext string
// 		strict     bool
// 	}{
// 		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "URYYB, JBEYQ!", false},
// 		{defaultPolyalphabeticAlphabet, "URYYB, JBEYQ!", "HELLO, WORLD!", false},
// 		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "URYYBJBEYQ", true},
// 		// {defaultPolyalphabeticAlphabet, "URYYB, JBEYQ!", "HELLOWORLD", true},
// 	}
// 	for _, table := range tables {
// 		c := NewRot13Cipher(table.alphabet)
// 		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
// 	}
// }
