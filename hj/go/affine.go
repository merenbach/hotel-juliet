package main

//todo: strict
//todo: param groups (caesar, atbash, etc)

import (
	"fmt"
	"strings"
)

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

func modulus(a, b int) int {
	// since the % is "remainder," not "modulus"...
	// work around https://github.com/golang/go/issues/448
	return ((a % b) + b) % b
}

func affine(x, a, b, m int) int {
	return modulus(a * x + b, m)
}

func invaffine(x, a, b, m int) int {
	modinv := mulinv(a, m)
	return modulus(modinv * (x - b), m)
}


type Message struct {
	text []rune
	alphabet string
}

func MakeMessageWithAlphabet(alphabet, s string) Message {
	return Message{[]rune(s), alphabet}
}

func MakeMessage(s string) Message {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	return MakeMessageWithAlphabet(alphabet, s)
}

func (msg Message) String() string {
	return string(msg.text)
}

func (msg Message) EncryptAffine(a, b int) Message {
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

func (msg Message) DecryptAffine(a, b int) Message {
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

func (msg Message) EncryptCaesar(b int) Message {
    return msg.EncryptAffine(1, b)
}

func (msg Message) DecryptCaesar(b int) Message {
    return msg.DecryptAffine(1, b)
}

func (msg Message) EncryptRot13() Message {
    return msg.EncryptCaesar(13)
}

func (msg Message) DecryptRot13() Message {
    return msg.DecryptCaesar(13)
}

func (msg Message) EncryptDecimation(a int) Message {
    return msg.EncryptAffine(a, 0)
}

func (msg Message) DecryptDecimation(a int) Message {
    return msg.DecryptAffine(a, 0)
}

func (msg Message) EncryptAtbash() Message {
    // Or use `len(msg.alphabet) - 1` for both fields
    return msg.EncryptAffine(-1, -1)
}

func (msg Message) DecryptAtbash() Message {
    // Or use `len(msg.alphabet) - 1` for both fields
    return msg.DecryptAffine(-1, -1)
}



func main() {
	fmt.Println("hello", affine(5,3,2,26))
    ptmsg := "hello, world"
    msg := MakeMessage(ptmsg)
msg2 := MakeMessage("abcdefghijklmnopqrstuvwxyz")
	enc1 := msg2.DecryptAtbash()
fmt.Println(enc1)
enc2 := enc1.DecryptRot13()
fmt.Println(enc2)
	fmt.Println(msg.EncryptCaesar(3))
//	fmt.Println(msg.EncryptAtbash())
//		msg = NewMessage("khoor, zruog")
//	fmt.Println(msg.DecryptCaesar(3))
}
