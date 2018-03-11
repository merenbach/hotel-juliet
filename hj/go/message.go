package main

import "fmt"

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

/*func (message Message) Chunk(int) Message {
	a
}*/

func (message Message) Transform(fn func(string) string) Message {
	return Message{Alphabet: message.Alphabet, Text: fn(message.Text)}
}
