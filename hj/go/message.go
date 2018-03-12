package main

import (
	"fmt"
	"strings"
)

type Message struct {
	Text     string
	Alphabet string
}

func (message Message) String() string {
	return fmt.Sprintf("Message (alphabet=%s): %s", message.Alphabet, message.Text)
}

// Chunk breaks up a copy of a Message into space-delimited chunks of a given size.
func (message Message) Chunk(sz int, alphabet string) Message {
	newRunes := make([]rune, 0)
	runeCount := 0
	SPACE := " "
	for _, c := range []rune(message.Text) {
		if strings.ContainsRune(alphabet, c) {
			newRunes = append(newRunes, c)
			runeCount += 1
			if runeCount%sz == 0 {
				newRunes = append(newRunes, []rune(SPACE)[0])
			}
		}
	}
	return Message{Alphabet: message.Alphabet, Text: string(newRunes)}
}

// Transform returns a copy of a Message transformed by a function.
func (message Message) Transform(fn func(string) string) Message {
	return Message{Alphabet: message.Alphabet, Text: fn(message.Text)}
}
