package main

import "testing"

const defaultMonoalphabeticAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runMonoalphabeticReciprocalTests(t *testing.T, plaintext, ciphertext string, c Cipher, strict bool) {
	encrypted := c.Encrypt(plaintext, strict)
	decrypted := c.Decrypt(ciphertext, strict)
	if string(encrypted) != ciphertext {
		t.Errorf("ciphertext %q was incorrect; wanted %q", encrypted, ciphertext)
	}
	if string(decrypted) != plaintext {
		t.Errorf("plaintext %q was incorrect; wanted: %q", decrypted, plaintext)
	}
}

// TestKeywordCipher tests the keyword cipher.
func TestKeywordCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		keyword    string
		strict     bool
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "CRHHL, WLQHG!", "KANGROOO", false},
		{defaultMonoalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO", false},
	}
	for _, table := range tables {
		c := NewKeywordCipher(table.alphabet, table.keyword)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestAffineCipher tests the affine cipher.
func TestAffineCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		a          int
		b          int
		strict     bool
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "AFCCX, BXSCY!", 7, 3, false},
		{defaultMonoalphabeticAlphabet, "IPQQJ, ZJCQA!", "HELLO, WORLD!", 7, 3, false},
	}
	for _, table := range tables {
		c := NewAffineCipher(table.alphabet, table.a, table.b)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)

	}
}

// TestAtbashCipher tests the Atbash cipher.
func TestAtbashCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		strict     bool
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "SVOOL, DLIOW!", false},
		{defaultMonoalphabeticAlphabet, "SVOOL, DLIOW!", "HELLO, WORLD!", false},
	}
	for _, table := range tables {
		c := NewAtbashCipher(table.alphabet)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestCaesarCipher tests the Caesar cipher.
func TestCaesarCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		b          int
		strict     bool
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "KHOOR, ZRUOG!", 3, false},
		{defaultMonoalphabeticAlphabet, "EBIIL, TLOIA!", "HELLO, WORLD!", 3, false},
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "YVCCF, NFICU!", 17, false},
		{defaultMonoalphabeticAlphabet, "QNUUX, FXAUM!", "HELLO, WORLD!", 17, false},
	}
	for _, table := range tables {
		c := NewCaesarCipher(table.alphabet, table.b)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestDecimationCipher tests the decimation cipher.
func TestDecimationCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		a          int
		strict     bool
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "XCZZU, YUPZV!", 7, false},
		{defaultMonoalphabeticAlphabet, "BIJJC, SCVJT!", "HELLO, WORLD!", 7, false},
	}
	for _, table := range tables {
		c := NewDecimationCipher(table.alphabet, table.a)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestRot13Cipher tests the Rot13 cipher.
func TestRot13Cipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		strict     bool
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "URYYB, JBEYQ!", false},
		{defaultMonoalphabeticAlphabet, "URYYB, JBEYQ!", "HELLO, WORLD!", false},
	}
	for _, table := range tables {
		c := NewRot13Cipher(table.alphabet)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}
