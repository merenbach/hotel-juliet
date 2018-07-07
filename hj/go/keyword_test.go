package main

import "testing"

const TEST_KEYWORD_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runKeywordReciprocalTests(t *testing.T, plaintext, ciphertext string, c Cipher) {
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
		{TEST_KEYWORD_ALPHABET, "HELLO, WORLD!", "CRHHL, WLQHG!", "KANGROOO"},
		{TEST_KEYWORD_ALPHABET, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO"},
	}
	for _, table := range tables {
		c := NewKeywordCipher(table.alphabet, table.keyword)
		runKeywordReciprocalTests(t, table.plaintext, table.ciphertext, c)
	}
}
