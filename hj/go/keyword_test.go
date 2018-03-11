package main

import "testing"

const TEST_KEYWORD_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runKeywordReciprocalTests(t *testing.T, cipher keywordCipher, plaintext, ciphertext string) {
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

func TestKeywordCipher(t *testing.T) {
	tables := []struct{
		plaintext string
		ciphertext string
		alphabet string
		keyword string
	}{
		{ "HELLO, WORLD!", "CRHHL, WLQHG!", TEST_KEYWORD_ALPHABET, "KANGAROO" },
		{ "LJOOF, WFEOI!", "HELLO, WORLD!", TEST_KEYWORD_ALPHABET, "KANGAROO" },
	}
	for _, table := range tables {
		cipher := MakeKeywordCipher(table.alphabet, table.keyword)
		runKeywordReciprocalTests(t, cipher, table.plaintext, table.ciphertext)
	}
}

