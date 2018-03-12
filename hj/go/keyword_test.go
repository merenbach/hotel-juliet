package main

import "testing"

const TEST_KEYWORD_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runKeywordReciprocalTests(t *testing.T, plaintext, ciphertext string, enc, dec func(string) string) {
	message := Message(plaintext)
	encrypted := message.Transform(enc)
	decrypted := encrypted.Transform(dec)
	if string(encrypted) != ciphertext {
		t.Errorf("Ciphertext was incorrect, got: %s, want: %s.", encrypted, ciphertext)
	}
	if string(decrypted) != plaintext {
		t.Errorf("Plaintext was incorrect, got: %s, want: %s.", decrypted, plaintext)
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
		keywordEncrypt := MakeKeywordEncrypt(table.alphabet, table.keyword)
		keywordDecrypt := MakeKeywordDecrypt(table.alphabet, table.keyword)
		runKeywordReciprocalTests(t, table.plaintext, table.ciphertext, keywordEncrypt, keywordDecrypt)
	}
}
