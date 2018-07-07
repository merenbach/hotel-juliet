package main

// // TabulaRecta holds a tabula recta.
// type TabulaRecta struct {
// 	keys       string
// 	ptAlphabet string
// 	tableaux   []tableau
// }

// func (tr TabulaRecta) String() string {
// 	out := make([]string, 0)
// 	formatForPrinting := func(s string) string {
// 		spl := strings.Split(s, "")
// 		return strings.Join(spl, " ")
// 	}
// 	out = append(out, formatForPrinting(tr.ptAlphabet))
// 	out = append(out, "-----")
// 	for _, t := range tr.tableaux {
// 		out = append(out, formatForPrinting(t.ctAlphabet))
// 	}
// 	fmt.Println(out)
// 	return strings.Join(out, "\n")
// }

// func NewTabulaRecta(ptAlphabet, ctAlphabet string) *TabulaRecta {
// 	tr := new(TabulaRecta)
// tr.ptAlphabet = ptAlphabet
// 	tr.tableaux = make([]tableau, len(ptAlphabet))
// 	for i := range ptAlphabet {
// 		a := MakeCaesarEncrypt(ctAlphabet, i)
// 		t := tableau{ptAlphabet, a(ctAlphabet)}
// 		tr.tableaux = append(tr.tableaux, t)
// 	}
// 	return tr
// }
