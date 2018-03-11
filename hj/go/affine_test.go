package main

import "testing"

const TEST_AFFINE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runAffineReciprocalTests(t *testing.T, alphabet string, plaintext, ciphertext string, enc, dec func(string) string) {
	message := Message{Alphabet: alphabet, Text: plaintext}
	encrypted := message.Transform(enc)
	decrypted := encrypted.Transform(dec)
	if encrypted.Text != ciphertext {
		t.Errorf("Ciphertext was incorrect, got: %s, want: %s.", encrypted.Text, ciphertext)
	}
	if decrypted.Text != plaintext {
		t.Errorf("Plaintext was incorrect, got: %s, want: %s.", decrypted.Text, plaintext)
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
		affineEncrypt := MakeAffineEncrypt(table.alphabet, table.a, table.b)
		affineDecrypt := MakeAffineDecrypt(table.alphabet, table.a, table.b)
		runAffineReciprocalTests(t, table.alphabet, table.plaintext, table.ciphertext, affineEncrypt, affineDecrypt)

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
		atbashEncrypt := MakeAtbashEncrypt(table.alphabet)
		atbashDecrypt := MakeAtbashDecrypt(table.alphabet)
		runAffineReciprocalTests(t, table.alphabet, table.plaintext, table.ciphertext, atbashEncrypt, atbashDecrypt)
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
		caesarEncrypt := MakeCaesarEncrypt(table.alphabet, table.b)
		caesarDecrypt := MakeCaesarDecrypt(table.alphabet, table.b)
		runAffineReciprocalTests(t, table.alphabet, table.plaintext, table.ciphertext, caesarEncrypt, caesarDecrypt)
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
		decimationEncrypt := MakeDecimationEncrypt(table.alphabet, table.a)
		decimationDecrypt := MakeDecimationDecrypt(table.alphabet, table.a)
		runAffineReciprocalTests(t, table.alphabet, table.plaintext, table.ciphertext, decimationEncrypt, decimationDecrypt)
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
		rot13Encrypt := MakeRot13Encrypt(table.alphabet)
		rot13Decrypt := MakeRot13Decrypt(table.alphabet)
		runAffineReciprocalTests(t, table.alphabet, table.plaintext, table.ciphertext, rot13Encrypt, rot13Decrypt)
	}
}
