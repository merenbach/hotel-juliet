package main

//todo: strict
//todo: param groups (caesar, atbash, etc)

import (
		"fmt"
		"strings"
	//	"math/big"
       )

func affine(x, a, b, m int) int {
	return (a * x + b) % m
}

// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
func xgcd(b, a int) (int, int, int) {
    x0, x1, y0, y1 := 1, 0, 0, 1
    for a != 0 {
        q := b / a
        b, a = a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    }
    return  b, x0, y0
}
// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
// return (g, x, y) a*x + b*y = gcd(x, y)
func egcd(a, b int) (int, int, int) {
    if a == 0 {
        return b, 0, 1
    } else {
        g, x, y := egcd(b % a, a)
        return g, y - (b / a) * x, x
    }
}
// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
// x = mulinv(b) mod n, (x * b) % n == 1
func mulinv(b, n int) int {
    g, x, _ := egcd(b, n)
    if g == 1 {
        return x % n
    }
return -1
}

func invaffine(x, a, b, m int) int {
modinv := mulinv(a, m)
// TODO: ensure b > 0
// work around https://github.com/golang/go/issues/448
for b > x {
b -= m
}
// might instead just do `b % m + m` below
return (modinv * (x - b)) % m
/*aprime := big.NewInt(int64(a))
//bprime := big.NewInt(b)
mprime := big.NewInt(int64(m))
modinv := new(big.Int).ModInverse(aprime, mprime)
	return (int(modinv.Int64()) * (x - b)) % m*/
}


type Message struct {
	text []rune
	alphabet string
}

func NewMessageWithAlphabet(alphabet, s string) (msg Message) {
    msg.text = []rune(s)
    msg.alphabet = alphabet
    return
}

func NewMessage(s string) (msg Message) {
    alphabet := "abcdefghijklmnopqrstuvwxyz"
    msg = NewMessageWithAlphabet(alphabet, s)
    return
}

func (msg *Message) String() string {
	return string(msg.text)
}

func (msg *Message) EncryptAffine(a, b int) *Message {
out := msg
	     for idx, rn := range msg.text {
			runeindex := strings.IndexRune(msg.alphabet, rn)
		   if runeindex != -1 {
		pos := affine(runeindex, a, b, len(msg.alphabet))
	     outrune := rune(msg.alphabet[pos])
	     out.text[idx] = outrune
		   }
	     }
	     return out
}

func (msg *Message) DecryptAffine(a, b int) *Message {
out := msg
	     for idx, rn := range msg.text {
			runeindex := strings.IndexRune(msg.alphabet, rn)
		   if runeindex != -1 {
		pos := invaffine(runeindex, a, b, len(msg.alphabet))
	     outrune := rune(msg.alphabet[pos])
	     out.text[idx] = outrune
		   }
	     }
	     return out
}

func (msg *Message) EncryptCaesar(b int) *Message {
    return msg.EncryptAffine(1, b)
}

func (msg *Message) DecryptCaesar(b int) *Message {
    return msg.DecryptAffine(1, b)
}

func (msg *Message) EncryptRot13() *Message {
    return msg.EncryptCaesar(13)
}

func (msg *Message) DecryptRot13() *Message {
    return msg.DecryptCaesar(13)
}

func (msg *Message) EncryptDecimation(a int) *Message {
    return msg.EncryptAffine(a, 0)
}

func (msg *Message) DecryptDecimation(a int) *Message {
    return msg.DecryptAffine(a, 0)
}

func (msg *Message) EncryptAtbash() *Message {
    coefficient := len(msg.alphabet) - 1
    return msg.EncryptAffine(coefficient, coefficient)
}

func (msg *Message) DecryptAtbash() *Message {
    coefficient := len(msg.alphabet) - 1
    return msg.DecryptAffine(coefficient, coefficient)
}



func main() {
	fmt.Println("hello", affine(5,3,2,26))
    ptmsg := "hello, world"
    msg := NewMessage(ptmsg)
msg2 := NewMessage("abcdefghijklmnopqrstuvwxyz")
	enc1 := msg2.EncryptRot13()
fmt.Println(enc1)
enc2 := enc1.DecryptRot13()
fmt.Println(enc2)
	fmt.Println(msg.EncryptCaesar(3))
//	fmt.Println(msg.EncryptAtbash())
//		msg = NewMessage("khoor, zruog")
//	fmt.Println(msg.DecryptCaesar(3))
}
