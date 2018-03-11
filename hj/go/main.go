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
