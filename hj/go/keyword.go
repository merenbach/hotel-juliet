package main

func makeKeywordAlphabets(alphabet1, alphabet2 string) ([]rune, []rune) {
	ptAlphabet := removeRuneDuplicates([]rune(alphabet1))
	ctAlphabet := removeRuneDuplicates([]rune(alphabet2))
	return ptAlphabet, ctAlphabet
}


func MakeKeywordEncrypt(alphabet, keyword string) (func(string) string) {
	ptAlphabet, ctAlphabet := makeKeywordAlphabets(alphabet, keyword + alphabet)
	xtable := ziprunes(ptAlphabet, ctAlphabet)
	return func(message string) string {
		return mapRuneTransform(message, xtable)
	}
}

func MakeKeywordDecrypt(alphabet, keyword string) (func(string) string) {
	ptAlphabet, ctAlphabet := makeKeywordAlphabets(alphabet, keyword + alphabet)
	xtable := ziprunes(ctAlphabet, ptAlphabet)
	return func(message string) string {
		return mapRuneTransform(message, xtable)
	}
}
