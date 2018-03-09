package main

//todo: strict
//todo: param groups (caesar, atbash, etc)
// TODO:
//  * additional unit tests, esp. with int'l charsets
//  * should alphabets be specified on encrypt/decrypt or on cipher creation?
//  * documentation
//  * formatting
//  * separate files
//  * strict mode
//  * multicase alphabets?
//  * multi value returns (e.g., out, error)
//  * keyword cipher
//  * polyalphabetic ciphers
//  * should we use pointers instead of values after all?... (probably not)
//  * also do interface, maybe, for enc/decrypt since not everything is affine based or monoalphabetic

import (
	"fmt"
	"strings"
)

/*type Cipher interface {
    encrypt() string
    decrypt() string
}*/

type affineCipher struct {
	alphabet string
	a int
	b int
}

func MakeAffineCipher(alphabet string, a, b int) affineCipher {
	return affineCipher{alphabet, a, b}
}

func MakeAtbashCipher(alphabet string) affineCipher {
	return MakeAffineCipher(alphabet, -1, -1)
}

func MakeCaesarCipher(alphabet string, b int) affineCipher {
	return MakeAffineCipher(alphabet, 1, b)
}

func MakeDecimationCipher(alphabet string, a int) affineCipher {
	return MakeAffineCipher(alphabet, a, 0)
}

func MakeRot13Cipher(alphabet string) affineCipher {
	return MakeCaesarCipher(alphabet, 13)
}

func (cipher affineCipher) Encrypt(message string) string {
	out := []rune(message)
	for idx, rn := range out {
		runeindex := strings.IndexRune(cipher.alphabet, rn)
		if runeindex != -1 {
			pos := affine(runeindex, cipher.a, cipher.b, len(cipher.alphabet))
			outrune := rune(cipher.alphabet[pos])
			out[idx] = outrune
		}
	}
	return string(out)
}

func (cipher affineCipher) Decrypt(message string) string {
	out := []rune(message)
	for idx, rn := range out {
		runeindex := strings.IndexRune(cipher.alphabet, rn)
		if runeindex != -1 {
			pos := invaffine(runeindex, cipher.a, cipher.b, len(cipher.alphabet))
		     	outrune := rune(cipher.alphabet[pos])
			out[idx] = outrune
		}
	}
	return string(out)
}

func (cipher affineCipher) String() string {
	return fmt.Sprintf("Affine Cipher (alphabet = %s, a = %d, b = %d)", cipher.alphabet, cipher.a, cipher.b)
}

func main() {
	fmt.Println("hello", affine(5,3,2,26))
c := MakeCaesarCipher("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 3)
fmt.Println(c)
fmt.Println(c.Encrypt("HELLOWORLD"))
//	fmt.Println(msg.EncryptAtbash())
//		msg = NewMessage("khoor, zruog")
//	fmt.Println(msg.DecryptCaesar(3))
}
