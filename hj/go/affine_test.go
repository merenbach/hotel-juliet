package main

import "testing"

const TEST_AFFINE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runAffineReciprocalTests(t *testing.T, plaintext, ciphertext string, c Cipher) {
	encrypted := c.Encrypt(plaintext, false)
	decrypted := c.Decrypt(ciphertext, false)
	if string(encrypted) != ciphertext {
		t.Errorf("ciphertext %q was incorrect; wanted %q", encrypted, ciphertext)
	}
	if string(decrypted) != plaintext {
		t.Errorf("plaintext %q was incorrect; wanted: %q", decrypted, plaintext)
	}
}

func TestAffineCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		a          int
		b          int
	}{
		{TEST_AFFINE_ALPHABET, "HELLO, WORLD!", "AFCCX, BXSCY!", 7, 3},
		{TEST_AFFINE_ALPHABET, "IPQQJ, ZJCQA!", "HELLO, WORLD!", 7, 3},
	}
	for _, table := range tables {
		c := NewAffineCipher(table.alphabet, table.a, table.b)
		runAffineReciprocalTests(t, table.plaintext, table.ciphertext, c)

	}
}

func TestAtbashCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
	}{
		{TEST_AFFINE_ALPHABET, "HELLO, WORLD!", "SVOOL, DLIOW!"},
		{TEST_AFFINE_ALPHABET, "SVOOL, DLIOW!", "HELLO, WORLD!"},
	}
	for _, table := range tables {
		c := NewAtbashCipher(table.alphabet)
		runAffineReciprocalTests(t, table.plaintext, table.ciphertext, c)
	}
}

func TestCaesarCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		b          int
	}{
		{TEST_AFFINE_ALPHABET, "HELLO, WORLD!", "KHOOR, ZRUOG!", 3},
		{TEST_AFFINE_ALPHABET, "EBIIL, TLOIA!", "HELLO, WORLD!", 3},
		{TEST_AFFINE_ALPHABET, "HELLO, WORLD!", "YVCCF, NFICU!", 17},
		{TEST_AFFINE_ALPHABET, "QNUUX, FXAUM!", "HELLO, WORLD!", 17},
	}
	for _, table := range tables {
		c := NewCaesarCipher(table.alphabet, table.b)
		runAffineReciprocalTests(t, table.plaintext, table.ciphertext, c)
	}
}

func TestDecimationCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		a          int
	}{
		{TEST_AFFINE_ALPHABET, "HELLO, WORLD!", "XCZZU, YUPZV!", 7},
		{TEST_AFFINE_ALPHABET, "BIJJC, SCVJT!", "HELLO, WORLD!", 7},
	}
	for _, table := range tables {
		c := NewDecimationCipher(table.alphabet, table.a)
		runAffineReciprocalTests(t, table.plaintext, table.ciphertext, c)
	}
}

func TestRot13Cipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
	}{
		{TEST_AFFINE_ALPHABET, "HELLO, WORLD!", "URYYB, JBEYQ!"},
		{TEST_AFFINE_ALPHABET, "URYYB, JBEYQ!", "HELLO, WORLD!"},
	}
	for _, table := range tables {
		c := NewRot13Cipher(table.alphabet)
		runAffineReciprocalTests(t, table.plaintext, table.ciphertext, c)
	}
}
