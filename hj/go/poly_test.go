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

// TestVigenereCipher tests the Vigenere cipher.
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

// TestVigenereTextAutoclaveCipher tests the Vigenere (text autoclave) cipher.
func TestVigenereTextAutoclaveCipher(t *testing.T) {
	tables := []struct {
		alphabet    string
		plaintext   string
		ciphertext  string
		countersign string
		strict      bool
	}{
		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "VGPLB, DSCWR!", "OCEANOGRAPHYWHAT"[:5], false},
		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "XLPWZ, KKFCO!", "Q", false},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO", false},
		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "CRHHLWLQHG", "KANGROOO", true},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLOWORLD", "KANGAROO", true},
	}
	for _, table := range tables {
		c := NewVigenereTextAutoclaveCipher(table.countersign, table.alphabet)
		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestVigenereKeyAutoclaveCipher tests the Vigenere (key autoclave) cipher.
func TestVigenereKeyAutoclaveCipher(t *testing.T) {
	tables := []struct {
		alphabet    string
		plaintext   string
		ciphertext  string
		countersign string
		strict      bool
	}{
		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "VGPLB, RUGWE!", "OCEANOGRAPHYWHAT"[:5], false},
		{defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "XBMXL, HVMXA!", "Q", false},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO", false},
		// {defaultPolyalphabeticAlphabet, "HELLO, WORLD!", "CRHHLWLQHG", "KANGROOO", true},
		// {defaultPolyalphabeticAlphabet, "LJOOF, WFEOI!", "HELLOWORLD", "KANGAROO", true},
	}
	for _, table := range tables {
		c := NewVigenereKeyAutoclaveCipher(table.countersign, table.alphabet)
		runPolyalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

// TestBeaufortCipher tests the Beaufort cipher.
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

// TestGronsfeldCipher tests the Gronsfeld cipher.
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

// TestTrithemiusCipher tests the Trithemius cipher.
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

// TestVariantBeaufortCipher tests the variant Beaufort cipher.
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

// TestReverseString tests the reverseString function.
func TestReverseString(t *testing.T) {
	table := map[string]string{
		"hello": "olleh",
		"world": "dlrow",
	}

	for k, v := range table {
		if o := reverseString(k); o != v {
			t.Errorf("Reverse of string %q was %q; expected %q", k, o, v)
		}
	}
}
