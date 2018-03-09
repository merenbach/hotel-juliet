package main

import "testing"

const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runReciprocalTests(t *testing.T, cipher affineCipher, plaintext, ciphertext string) {
	encrypted := cipher.Encrypt(plaintext)
	decrypted := cipher.Decrypt(ciphertext)
	unencrypted := cipher.Decrypt(encrypted)
	undecrypted := cipher.Encrypt(decrypted)
	if encrypted != ciphertext {
		t.Errorf("Ciphertext was incorrect, got: %s, want: %s.", encrypted, ciphertext)
	}
	if decrypted != plaintext {
		t.Errorf("Plaintext was incorrect, got: %s, want: %s.", decrypted, plaintext)
	}
	if unencrypted != plaintext {
		t.Errorf("Reverse operation on original encryption was incorrect, got: %s, want: %s.", unencrypted, plaintext)
	}
	if undecrypted != ciphertext {
		t.Errorf("Reverse operation on original decryption was incorrect, got: %s, want: %s.", undecrypted, ciphertext)
	}
}

func TestAffineCipher(t *testing.T) {
	tables := []struct{
		plaintext string
		ciphertext string
		a int
		b int
	}{
		{ "HELLO, WORLD!", "AFCCX, BXSCY!", 7, 3 },
		{ "IPQQJ, ZJCQA!", "HELLO, WORLD!", 7, 3 },
	}
	for _, table := range tables {
		cipher := MakeAffineCipher(ALPHABET, table.a, table.b)
		runReciprocalTests(t, cipher, table.plaintext, table.ciphertext)
	}
}

func TestAtbashCipher(t *testing.T) {
	tables := []struct{
		plaintext string
		ciphertext string
	}{
		{ "HELLO, WORLD!", "SVOOL, DLIOW!" },
		{ "SVOOL, DLIOW!", "HELLO, WORLD!" },
	}
	for _, table := range tables {
		cipher := MakeAtbashCipher(ALPHABET)
		runReciprocalTests(t, cipher, table.plaintext, table.ciphertext)
	}
}

func TestCaesarCipher(t *testing.T) {
	tables := []struct{
		plaintext string
		ciphertext string
		b int
	}{
		{ "HELLO, WORLD!", "KHOOR, ZRUOG!", 3 },
		{ "EBIIL, TLOIA!", "HELLO, WORLD!", 3 },
		{ "HELLO, WORLD!", "YVCCF, NFICU!", 17 },
		{ "QNUUX, FXAUM!", "HELLO, WORLD!", 17 },
	}
	for _, table := range tables {
		cipher := MakeCaesarCipher(ALPHABET, table.b)
		runReciprocalTests(t, cipher, table.plaintext, table.ciphertext)
	}
}

func TestDecimationCipher(t *testing.T) {
	tables := []struct{
		plaintext string
		ciphertext string
		a int
	}{
		{ "HELLO, WORLD!", "XCZZU, YUPZV!", 7 },
		{ "BIJJC, SCVJT!", "HELLO, WORLD!", 7 },
	}
	for _, table := range tables {
		cipher := MakeDecimationCipher(ALPHABET, table.a)
		runReciprocalTests(t, cipher, table.plaintext, table.ciphertext)
	}
}

func TestRot13Cipher(t *testing.T) {
	tables := []struct{
		plaintext string
		ciphertext string
	}{
		{ "HELLO, WORLD!", "URYYB, JBEYQ!" },
		{ "URYYB, JBEYQ!", "HELLO, WORLD!" },
	}
	for _, table := range tables {
		cipher := MakeRot13Cipher(ALPHABET)
		runReciprocalTests(t, cipher, table.plaintext, table.ciphertext)
	}
}

