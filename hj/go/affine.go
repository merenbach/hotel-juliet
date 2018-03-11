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
"math/big"
)


// TODO: Needs error option or ok option
// affine returns the result of `(ax + b) mod m`
// TODO: enforce constraints such as m > 0
// https://en.wikipedia.org/wiki/Linear_congruential_generator
func makeAffine(m, a, b int) (func() *big.Int) {
   m_, a_, b_ := int64(m), int64(a), int64(b)
   f, _ := makeLCG(big.NewInt(m_), big.NewInt(1), big.NewInt(a_), big.NewInt(b_))
   return f
}

/*func affine(x, a, b, m int) int {
	return Modulus(a * x + b, m)
}

func invaffine(x, a, b, m int) int {
	modinv := mulinv(a, m)
	return Modulus(modinv * (x - b), m)
}/*

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
	ab := len([]rune(alphabet)) - 1
	return MakeAffineCipher(alphabet, ab, ab)
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
func (cipher affineCipher) transform(alphabet []rune, fn func () *big.Int) []rune {
	out := make([]rune, 0)
	for range alphabet {
		pos := fn().Int64()
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
	myfn := makeAffine(len(ptalphabet), cipher.a, cipher.b)
	ctalphabet := cipher.transform(ptalphabet, myfn)
	xtable := ziprunes(ptalphabet, ctalphabet)
	return cipher.transcode(message, xtable)
}

func (cipher affineCipher) Decrypt(message string) string {
	ptalphabet := []rune(cipher.alphabet)
	myfn := makeAffine(len(ptalphabet), cipher.a, cipher.b)
	ctalphabet := cipher.transform(ptalphabet, myfn)
	xtable := ziprunes(ctalphabet, ptalphabet)
	return cipher.transcode(message, xtable)
}

func (cipher affineCipher) String() string {
	return fmt.Sprintf("Affine Cipher (alphabet = %s, a = %d, b = %d)", cipher.alphabet, cipher.a, cipher.b)
}

func main() {
	//fmt.Println("hello", affine(5,3,2,26))
fn := makeAffine(26, 1, 3)
for i:=0;i<52;i++ {
fmt.Print(fn(), " ")
}
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
