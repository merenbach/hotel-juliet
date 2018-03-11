package main

import "testing"

const TEST_KEYWORD_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runKeywordReciprocalTests(t *testing.T, alphabet string, plaintext, ciphertext string, enc, dec func(string) string) {
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

func TestKeywordCipher(t *testing.T) {
	tables := []struct{
		alphabet string
		plaintext string
		ciphertext string
		keyword string
	}{
		{ TEST_KEYWORD_ALPHABET, "HELLO, WORLD!", "CRHHL, WLQHG!", "KANGROOO" },
		{ TEST_KEYWORD_ALPHABET, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO" },
	}
	for _, table := range tables {
		keywordEncrypt := MakeKeywordEncrypt(table.alphabet, table.keyword)
		keywordDecrypt := MakeKeywordDecrypt(table.alphabet, table.keyword)
		runKeywordReciprocalTests(t, table.alphabet, table.plaintext, table.ciphertext, keywordEncrypt, keywordDecrypt)
	}
}

