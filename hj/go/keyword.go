package main

func makeKeywordTableau(alphabet1, alphabet2 string) tableau {
	ptAlphabet := removeRuneDuplicates([]rune(alphabet1))
	ctAlphabet := removeRuneDuplicates([]rune(alphabet2))
	return MakeTableau(string(ptAlphabet), string(ctAlphabet))
}

func MakeKeywordEncrypt(alphabet, keyword string) func(string) string {
	tableau := makeKeywordTableau(alphabet, keyword+alphabet)
	return tableau.Pt2Ct()
}

func MakeKeywordDecrypt(alphabet, keyword string) func(string) string {
	tableau := makeKeywordTableau(alphabet, keyword+alphabet)
	return tableau.Ct2Pt()
}
