package main

import (
	"fmt"
	"strings"
)

type Cipher interface {
	Encrypt(string) string
	Decrypt(string) string
}

type Message struct {
	Text     string
	Alphabet string
}

func (message Message) String() string {
	return fmt.Sprintf("Message (alphabet=%s): %s", message.Alphabet, message.Text)
}

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

func (message Message) Transform(fn func(string) string) Message {
	return Message{Alphabet: message.Alphabet, Text: fn(message.Text)}
}
