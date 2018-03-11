package main


import (
	"fmt"
)

type keywordCipher struct {
	ptAlphabet string
	ctAlphabet string
	keyword string
}

func MakeKeywordCipher(alphabet, keyword string) keywordCipher {
	ctAlphabet := removeDupes(keyword + alphabet)
	return keywordCipher{alphabet, ctAlphabet, keyword}
}

func removeDupes(s string) string {
	seen := make([]rune, 0)
	seenMap := make(map[rune]bool)

	for _, e := range []rune(s) {
		if _, ok := seenMap[e]; !ok {
			seen = append(seen, e)
			seenMap[e] = true
		}
	}
	return string(seen)
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
	xtable := ziprunes([]rune(cipher.ptAlphabet), []rune(cipher.ctAlphabet))
	return cipher.transcode(message, xtable)
}

func (cipher keywordCipher) Decrypt(message string) string {
	xtable := ziprunes([]rune(cipher.ctAlphabet), []rune(cipher.ptAlphabet))
	return cipher.transcode(message, xtable)
}

func (cipher keywordCipher) String() string {
	return fmt.Sprintf("Keyword Cipher (ptAlphabet = %s, ctAlphabet = %s, keyword = %s)", cipher.ptAlphabet, cipher.ctAlphabet, cipher.keyword)
}
