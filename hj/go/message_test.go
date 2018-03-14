package main

import "testing"

func TestMessageConstrain(t *testing.T) {
	alphabet := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	tables := []struct {
		text     string
		charset  string
		expected string
	}{
		{"HELLO, WORLD!", alphabet, "HELLOWORLD"},
		{"Hello, world!", alphabet, "H"},
		{"HELLO, WORLD!", "HELLO, WORLD!", "HELLO, WORLD!"},
		{alphabet, "HELLO, WORLD!", "DEHLORW"},
	}
	for _, table := range tables {
		message := Message(table.text)
		if output := message.ConstrainRunes(table.charset); string(output) != table.expected {
			t.Errorf("Constraining runes on \"%s\" to \"%s\" incorrect. Received: %s; expected: %s", table.text, table.charset, string(output), table.expected)
		}
	}
}
