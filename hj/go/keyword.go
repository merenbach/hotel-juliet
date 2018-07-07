package main

func rmStringDuplicates(s string) string {
	out := removeRuneDuplicates([]rune(s))
	return string(out)
}

func MakeSimpleTableauForKeyword(alphabet, keyword string) Cipher {
	ctAlphabet := rmStringDuplicates(keyword + alphabet)
	return MakeSimpleTableau(alphabet, ctAlphabet)
}
