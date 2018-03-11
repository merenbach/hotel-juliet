package main


import (
	"fmt"
)

type keywordCipher struct {
	alphabet string
	keyword string
}

func MakeKeywordCipher(alphabet, keyword string) keywordCipher {
	return keywordCipher{alphabet, keyword}
}

func (cipher keywordCipher) transcode(message string, xtable map[rune]rune) string {
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

func (cipher keywordCipher) Encrypt(message string) string {
	ptalphabet := []rune(cipher.alphabet)
	ctalphabet := []rune(cipher.keyword + cipher.alphabet)
	xtable := ziprunes(ptalphabet, ctalphabet)
	return cipher.transcode(message, xtable)
}

func (cipher keywordCipher) Decrypt(message string) string {
	ptalphabet := []rune(cipher.alphabet)
	ctalphabet := []rune(cipher.keyword + cipher.alphabet)
	xtable := ziprunes(ctalphabet, ptalphabet)
	return cipher.transcode(message, xtable)
}

func (cipher keywordCipher) String() string {
	return fmt.Sprintf("Keyword Cipher (alphabet = %s, keyword = %s)", cipher.alphabet, cipher.keyword)
}
