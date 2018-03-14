package main

import (
	"fmt"
	"strings"
)

type Message string

func (message Message) String() string {
	return fmt.Sprintf("Message: %s", string(message))
}

// Chunk breaks up a copy of a Message into space-delimited chunks of a given size.
func (message Message) Chunk(sz int, alphabet string) Message {
	newRunes := make([]rune, 0)
	runeCount := 0
	SPACE := " "
	for _, c := range []rune(string(message)) {
		if strings.ContainsRune(alphabet, c) {
			newRunes = append(newRunes, c)
			runeCount += 1
			if runeCount%sz == 0 {
				newRunes = append(newRunes, []rune(SPACE)[0])
			}
		}
	}
	return Message(newRunes)
}

// ConstrainRunes returns a copy of a message containing only runes shared with the provided character set.
func (message Message) ConstrainRunes(charset string) Message {
	out := make([]rune, 0)
	for _, e := range message {
		if strings.ContainsRune(charset, e) {
			out = append(out, e)
		}
	}
	return Message(out)
}

// Transform returns a copy of a Message transformed by a function.
func (message Message) Transform(fn func(string) string) Message {
	return Message(fn(string(message)))
}
