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
)

// affine returns the result of `(ax + b) mod m`
// TODO: Needs error option or ok option
// TODO: just use an LCG function?
func affine(x, a, b, m int) int {
	return Modulus(a * x + b, m)
}

func invaffine(x, a, b, m int) int {
	modinv := mulinv(a, m)
	return Modulus(modinv * (x - b), m)
}

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

/*
func (cipher affineCipher) transcode(message string, fn func (int, int, int, int) int) string {
	out := make([]rune, len(message))
	for _, rn := range []rune(message) {
		runeindex := strings.IndexRune(cipher.alphabet, rn)
		if runeindex != -1 {
			pos := fn(runeindex, cipher.a, cipher.b, len(cipher.alphabet))
			outrune := rune(cipher.alphabet[pos])
			out = append(out, outrune)
		}
	}
	return string(out)
}*/

func ziprunes(a, b []rune) map[rune]rune {
	out := make(map[rune]rune)
	for i, e := range a {
		out[e] = b[i]
	}
	return out
}

// run fn on range(0..len of alphabet) to produce OUTARRAY []int
// then zip (a) with a[OUTARRAY[current element of a]]

// transform transforms a rune array (alphabet) based on a function
func (cipher affineCipher) transform(alphabet []rune, fn func (int) int) []rune {
	out := make([]rune, 0)
	for i := range alphabet {
		pos := fn(i)
		out = append(out, alphabet[pos])
	}
	return out
}

func (cipher affineCipher) transcode(message string, xtable map[rune]rune) string {
	out := make([]rune, 0)
	for _, rn := range []rune(message) {
		xcoded, ok := xtable[rn]
		if !ok {
			xcoded = rn
		}
		out = append(out, xcoded)
	}
	return string(out)
}

func (cipher affineCipher) Encrypt(message string) string {
	ptalphabet := []rune(cipher.alphabet)
	myfn := func(i int) int { return affine(i, cipher.a, cipher.b, len(ptalphabet)) }
	ctalphabet := cipher.transform(ptalphabet, myfn)
	xtable := ziprunes(ptalphabet, ctalphabet)
	return cipher.transcode(message, xtable)
}

func (cipher affineCipher) Decrypt(message string) string {
	ptalphabet := []rune(cipher.alphabet)
	myfn := func(i int) int { return affine(i, cipher.a, cipher.b, len(ptalphabet)) }
	ctalphabet := cipher.transform(ptalphabet, myfn)
	xtable := ziprunes(ctalphabet, ptalphabet)
	return cipher.transcode(message, xtable)
}

func (cipher affineCipher) String() string {
	return fmt.Sprintf("Affine Cipher (alphabet = %s, a = %d, b = %d)", cipher.alphabet, cipher.a, cipher.b)
}

func main() {
	fmt.Println("hello", affine(5,3,2,26))
	alphabet := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	c := MakeCaesarCipher(alphabet, 3)
//	mymap := ziprunes([]rune(alphabet), []rune("QADCFGBEZIJKLMNOPRSTUVWXYH"))
//	fmt.Println(mymap)
/*	myfn := func(s string, outpipe chan rune) {
		for i, x := range s {
			
		}
	}
	o := makeXtable(alphabet, myfn)
	fmt.Println(o)*/
fmt.Println(c)
fmt.Println(c.Encrypt("HELLOWORLD"))
//	fmt.Println(msg.DecryptCaesar(3))
}
