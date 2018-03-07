package main

//todo: strict
//todo: param groups (caesar, atbash, etc)

import (
		"fmt"
		"strings"
		"math/big"
       )

func affine(x, a, b, m int) int {
	return (a * x + b) % m
}
func invaffine(x, a, b, m int) int {
aprime := big.NewInt(int64(a))
//bprime := big.NewInt(b)
mprime := big.NewInt(int64(m))
modinv := new(big.Int).ModInverse(aprime, mprime)
	return (int(modinv.Int64()) * (x - b)) % m
}


type Message struct {
	text string
		alphabet string
}

func (msg *Message) String() string {
	return msg.text
}

func (msg *Message) Encrypt() *Message {
out := msg
	     runiedumplings := []rune(msg.text)
	     for idx, rn := range msg.text {
			runeindex := strings.IndexRune(msg.alphabet, rn)
		   if runeindex != -1 {
		pos := affine(runeindex, 1, 3, len(msg.alphabet))
	     outrune := rune(msg.alphabet[pos])
	     runiedumplings[idx] = outrune
		   }
	     }
     out.text = string(runiedumplings)
	     return out
}

func (msg *Message) Decrypt() *Message {
out := msg
	     runiedumplings := []rune(msg.text)
	     for idx, rn := range msg.text {
			runeindex := strings.IndexRune(msg.alphabet, rn)
		   if runeindex != -1 {
		pos := invaffine(runeindex, 1, 3, len(msg.alphabet))
	     outrune := rune(msg.alphabet[pos])
	     runiedumplings[idx] = outrune
		   }
	     }
     out.text = string(runiedumplings)
	     return out
}

func main() {
	fmt.Println("hello", affine(5,3,2,26))
		msg := &Message{text:"hello, world", alphabet:"abcdefghijklmnopqrstuvwxyz"}
	fmt.Println(msg.Encrypt())
		msg = &Message{text:"khoor, zruog", alphabet:"abcdefghijklmnopqrstuvwxyz"}
	fmt.Println(msg.Decrypt())
}
