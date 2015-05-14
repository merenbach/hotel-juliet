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

if __name__ == '__main__':
    unittest.main()
