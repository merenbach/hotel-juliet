package main

import (
	"fmt"
)

// Message holds a message string.
type Message string

func (message Message) String() string {
	return fmt.Sprintf("Message: %s", string(message))
}

// Chunk breaks up a copy of a Message into space-delimited chunks of a given size.
// TODO: end padding with null
// TODO: farm this out to a stringutil function
func (message Message) Chunk(sz int, alphabet string) Message {
	const SPACE = ' '
	msg := string(message.ConstrainRunes(alphabet))
	out := chunk(msg, sz, SPACE)
	return Message(out)
}

// ConstrainRunes returns a copy of a message containing only runes shared with the provided character set.
func (message Message) ConstrainRunes(charset string) Message {
	return Message(intersect(string(message), charset))
}

// Transform returns a copy of a Message transformed by a function.
func (message Message) Transform(fn func(string) string) Message {
	return Message(fn(string(message)))
}
