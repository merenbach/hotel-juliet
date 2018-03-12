package main

//todo: strict
//todo: param groups (caesar, atbash, etc)
// TODO:
//  * additional unit tests, esp. with int'l charsets
//  * should alphabets be specified on encrypt/decrypt or on cipher creation?
//  * documentation
//  * formatting
//  * separate files
//  * strict mode: on new Message struct type
//  * should be able to print out cipher alphabet tableaux
//  * multicase alphabets?
//  * multi value returns (e.g., out, error)
//  * keyword cipher
//  * polyalphabetic ciphers
//  * should we use pointers instead of values after all?... (probably not)
//  * also do interface, maybe, for enc/decrypt since not everything is affine based or monoalphabetic

import (
	"fmt"
)

func main() {
	m := Message("HELLO, WORLD!")
	m2 := m.Chunk(5, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
	c := MakeCaesarEncrypt("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 3)
	m2 = m.Transform(c)
	fmt.Println("Hello, world!", m, m2)
}
