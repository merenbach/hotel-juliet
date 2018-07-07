package main

import "testing"

const defaultMonoalphabeticAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runMonoalphabeticReciprocalTests(t *testing.T, plaintext, ciphertext string, c Cipher) {
	encrypted := c.Encrypt(plaintext, false)
	decrypted := c.Decrypt(ciphertext, false)
	if string(encrypted) != ciphertext {
		t.Errorf("ciphertext %q was incorrect; wanted %q", encrypted, ciphertext)
	}
	if string(decrypted) != plaintext {
		t.Errorf("plaintext %q was incorrect; wanted: %q", decrypted, plaintext)
	}
}

func TestKeywordCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		keyword    string
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "CRHHL, WLQHG!", "KANGROOO"},
		{defaultMonoalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO"},
	}
	for _, table := range tables {
		c := NewKeywordCipher(table.alphabet, table.keyword)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c)
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
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "AFCCX, BXSCY!", 7, 3},
		{defaultMonoalphabeticAlphabet, "IPQQJ, ZJCQA!", "HELLO, WORLD!", 7, 3},
	}
	for _, table := range tables {
		c := NewAffineCipher(table.alphabet, table.a, table.b)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c)

	}
}

func TestAtbashCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "SVOOL, DLIOW!"},
		{defaultMonoalphabeticAlphabet, "SVOOL, DLIOW!", "HELLO, WORLD!"},
	}
	for _, table := range tables {
		c := NewAtbashCipher(table.alphabet)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c)
	}
}

func TestCaesarCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		b          int
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "KHOOR, ZRUOG!", 3},
		{defaultMonoalphabeticAlphabet, "EBIIL, TLOIA!", "HELLO, WORLD!", 3},
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "YVCCF, NFICU!", 17},
		{defaultMonoalphabeticAlphabet, "QNUUX, FXAUM!", "HELLO, WORLD!", 17},
	}
	for _, table := range tables {
		c := NewCaesarCipher(table.alphabet, table.b)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c)
	}
}

func TestDecimationCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		a          int
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "XCZZU, YUPZV!", 7},
		{defaultMonoalphabeticAlphabet, "BIJJC, SCVJT!", "HELLO, WORLD!", 7},
	}
	for _, table := range tables {
		c := NewDecimationCipher(table.alphabet, table.a)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c)
	}
}

func TestRot13Cipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "URYYB, JBEYQ!"},
		{defaultMonoalphabeticAlphabet, "URYYB, JBEYQ!", "HELLO, WORLD!"},
	}
	for _, table := range tables {
		c := NewRot13Cipher(table.alphabet)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c)
	}
}
