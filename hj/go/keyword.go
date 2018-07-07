package main

func rmStringDuplicates(s string) string {
	out := removeRuneDuplicates([]rune(s))
	return string(out)
}

func NewKeywordCipher(alphabet, keyword string) Cipher {
	ctAlphabet := rmStringDuplicates(keyword + alphabet)
	return NewSimpleTableau(alphabet, ctAlphabet)
}
