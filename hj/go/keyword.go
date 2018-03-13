package main

func makeKeywordAlphabets(alphabet1, alphabet2 string) (string, string) {
	ptAlphabet := removeRuneDuplicates([]rune(alphabet1))
	ctAlphabet := removeRuneDuplicates([]rune(alphabet2))
	return string(ptAlphabet), string(ctAlphabet)
}

func MakeKeywordEncrypt(alphabet, keyword string) func(string) string {
	ptAlphabet, ctAlphabet := makeKeywordAlphabets(alphabet, keyword+alphabet)
	tableau := MakeTableau(ptAlphabet, ctAlphabet)
	return tableau.Pt2Ct()
}

func MakeKeywordDecrypt(alphabet, keyword string) func(string) string {
	ptAlphabet, ctAlphabet := makeKeywordAlphabets(alphabet, keyword+alphabet)
	tableau := MakeTableau(ptAlphabet, ctAlphabet)
	return tableau.Ct2Pt()
}
