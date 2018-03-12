# Hotel Juliet (Go version)

## How to use (WIP)

// import hotel juliet up here

    m := Message("HELLO, WORLD!")
    alphabet := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    enc := MakeCaesarEncrypt(alphabet, 3)
    dec := MakeCaesarEncrypt(alphabet, 3)

    // becomes: KHOOR, ZRUOG!
    m2 := m.Transform(enc)

    // back to: HELLO, WORLD!
    m3 := m2.Transform(dec)

