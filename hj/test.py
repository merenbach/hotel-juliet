#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ciphers import *

TEST_MESSAGE = 'HELLO, WORLD!'

# class AlphabetTest(unittest.TestCase):
#     def test_rotate(self):
#         ab = Alphabet()
#         for i in range(0, len(ab)):
#             rot_left = ab.rotated(i)
#             rot_right = ab.rotated(-i)


class CipherTest(unittest.TestCase):
    def test_caesarcipher(self):
        c = CaesarCipher()
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'KHOOR, ZRUOG!')
        self.assertEqual(TEST_MESSAGE, d)

    def test_caesarcipher_reverse(self):
        c = CaesarCipher()
        e = c.decode('HELLO, WORLD!')
        d = c.encode(e)
        self.assertEqual(e, 'EBIIL, TLOIA!')
        self.assertEqual(TEST_MESSAGE, d)

    def test_atbashcipher(self):
        c = AtbashCipher()
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'SVOOL, DLIOW!')
        self.assertEqual(TEST_MESSAGE, d)

    def test_atbashcipher_reverse(self):
        c = AtbashCipher()
        e = c.decode('HELLO, WORLD!')
        d = c.encode(e)
        self.assertEqual(e, 'SVOOL, DLIOW!')
        self.assertEqual(TEST_MESSAGE, d)

    def test_keywordcipher(self):
        c = KeywordCipher(keyword='KANGAROO')
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'CRHHL, WLQHG!')
        self.assertEqual(TEST_MESSAGE, d)

    def test_keywordcipher_reverse(self):
        c = KeywordCipher(keyword='KANGAROO')
        e = c.decode('HELLO, WORLD!')
        d = c.encode(e)
        self.assertEqual(e, 'LJOOF, WFEOI!')
        self.assertEqual(TEST_MESSAGE, d)

    def test_affinecipher(self):
        c = AffineCipher(7, 3)
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'AFCCX, BXSCY!')
        self.assertEqual(TEST_MESSAGE, d)

    def test_affinecipher_reverse(self):
        c = AffineCipher(7, 3)
        e = c.decode('HELLO, WORLD!')
        d = c.encode(e)
        self.assertEqual(e, 'IPQQJ, ZJCQA!')
        self.assertEqual(TEST_MESSAGE, d)


class PolyCipherTest(unittest.TestCase):
    PASSPHRASE = 'OCEANOGRAPHYWHAT'

    def test_vigenere(self):
        c = VigenereCipher(self.PASSPHRASE)
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'VGPLB, KUILS!')
        self.assertEqual('HELLO, WORLD!', d)

    def test_vigenere_reverse(self):
        c = VigenereCipher(self.PASSPHRASE)
        e = c.decode('HELLO, WORLD!')
        d = c.encode(e)
        self.assertEqual(e, 'TCHLB, IIALO!')
        self.assertEqual('HELLO, WORLD!', d)

    def test_variantbeaufort(self):
        c = VariantBeaufortCipher(self.PASSPHRASE)
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'TCHLB, IIALO!')
        self.assertEqual('HELLO, WORLD!', d)

    def test_variantbeaufort_reverse(self):
        c = VariantBeaufortCipher(self.PASSPHRASE)
        e = c.decode('HELLO, WORLD!')
        d = c.encode(e)
        self.assertEqual(e, 'VGPLB, KUILS!')
        self.assertEqual('HELLO, WORLD!', d)

    def test_trithemius(self):
        c = TrithemiusCipher()
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'HFNOS, BUYTM!')
        self.assertEqual('HELLO, WORLD!', d)

    def test_trithemius_reverse(self):
        c = TrithemiusCipher()
        e = c.decode('HELLO, WORLD!')
        d = c.encode(e)
        self.assertEqual(e, 'HDJIK, RIKDU!')
        self.assertEqual('HELLO, WORLD!', d)

    def test_beaufort(self):
        c = BeaufortCipher(self.PASSPHRASE)
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'HYTPZ, SSAPM!')
        self.assertEqual('HELLO, WORLD!', d)

    def test_beaufort_reverse(self):
        c = BeaufortCipher(self.PASSPHRASE)
        e = c.decode('HELLO, WORLD!')
        d = c.encode(e)
        self.assertEqual(e, 'HYTPZ, SSAPM!')
        self.assertEqual('HELLO, WORLD!', d)

    def test_gronsfeld(self):
        c = GronsfeldCipher(passphrase='23132')
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'JHMOQ, YRSOF!')
        self.assertEqual('HELLO, WORLD!', d)

    def test_gronsfeld_reverse(self):
        c = GronsfeldCipher(passphrase='23132')
        e = c.decode('HELLO, WORLD!')
        d = c.encode(e)
        self.assertEqual(e, 'FBKIM, ULQIB!')
        self.assertEqual('HELLO, WORLD!', d)

if __name__ == '__main__':
    unittest.main()
