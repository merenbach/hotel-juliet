package main

import (
	"reflect"
	"testing"
)

const defaultMonoalphabeticAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func runMonoalphabeticReciprocalTests(t *testing.T, plaintext, ciphertext string, c Cipher, strict bool) {
	encrypted := c.Encipher(plaintext, strict)
	decrypted := c.Decipher(ciphertext, strict)
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
		strict     bool
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "CRHHL, WLQHG!", "KANGROOO", false},
		{defaultMonoalphabeticAlphabet, "LJOOF, WFEOI!", "HELLO, WORLD!", "KANGAROO", false},
		// {defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "CRHHLWLQHG", "KANGROOO", true},
		// {defaultMonoalphabeticAlphabet, "LJOOF, WFEOI!", "HELLOWORLD", "KANGAROO", true},
	}
	for _, table := range tables {
		c := NewKeywordCipher(table.alphabet, table.keyword)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

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
		// {defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "AFCCXBXSCY", 7, 3, true},
		// {defaultMonoalphabeticAlphabet, "IPQQJ, ZJCQA!", "HELLOWORLD", 7, 3, true},
	}
	for _, table := range tables {
		c := NewAffineCipher(table.alphabet, table.a, table.b)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)

	}
}

func TestAtbashCipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		strict     bool
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "SVOOL, DLIOW!", false},
		{defaultMonoalphabeticAlphabet, "SVOOL, DLIOW!", "HELLO, WORLD!", false},
		// {defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "SVOOLDLIOW", true},
		// {defaultMonoalphabeticAlphabet, "SVOOL, DLIOW!", "HELLOWORLD", true},
	}
	for _, table := range tables {
		c := NewAtbashCipher(table.alphabet)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

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
		// {defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "KHOORZRUOG", 3, true},
		// {defaultMonoalphabeticAlphabet, "EBIIL, TLOIA!", "HELLOWORLD", 3, true},
		// {defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "YVCCFNFICU", 17, true},
		// {defaultMonoalphabeticAlphabet, "QNUUX, FXAUM!", "HELLOWORLD", 17, true},
	}
	for _, table := range tables {
		c := NewCaesarCipher(table.alphabet, table.b)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

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
		// {defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "XCZZUYUPZV", 7, true},
		// {defaultMonoalphabeticAlphabet, "BIJJC, SCVJT!", "HELLOWORLD", 7, true},
	}
	for _, table := range tables {
		c := NewDecimationCipher(table.alphabet, table.a)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

func TestRot13Cipher(t *testing.T) {
	tables := []struct {
		alphabet   string
		plaintext  string
		ciphertext string
		strict     bool
	}{
		{defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "URYYB, JBEYQ!", false},
		{defaultMonoalphabeticAlphabet, "URYYB, JBEYQ!", "HELLO, WORLD!", false},
		// {defaultMonoalphabeticAlphabet, "HELLO, WORLD!", "URYYBJBEYQ", true},
		// {defaultMonoalphabeticAlphabet, "URYYB, JBEYQ!", "HELLOWORLD", true},
	}
	for _, table := range tables {
		c := NewRot13Cipher(table.alphabet)
		runMonoalphabeticReciprocalTests(t, table.plaintext, table.ciphertext, c, table.strict)
	}
}

func TestBackpermute(t *testing.T) {
	tables := []struct {
		expected string
		s        string
		f        func() uint
	}{
		{"eeeee", "hello", func() uint { return 1 }},
	}
	for _, table := range tables {
		if out := backpermute(table.s, table.f); out != table.expected {
			t.Errorf("for backpermutation of %q with function %s, expected output %q, but got %q instead", table.s, reflect.ValueOf(table.f), table.expected, out)
		}
	}
}

func TestDeduplicateString(t *testing.T) {
	table := map[string]string{
		"hello":       "helo",
		"world":       "world",
		"hello world": "helo wrd",
	}

	for k, v := range table {
		if o := deduplicateString(k); o != v {
			t.Errorf("deduplication of string %q was %q; expected %q", k, o, v)
		}
	}
}
