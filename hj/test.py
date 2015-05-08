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
        c = CaesarShiftCipher()
        e = c.encode('HELLO, WORLD!')
        d = c.decode(e)
        self.assertEqual(e, 'KHOOR, ZRUOG!')
        self.assertEqual(TEST_MESSAGE, d)

    def test_caesarcipher_reverse(self):
        c = CaesarShiftCipher()
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

if __name__ == '__main__':
    unittest.main()



#
# from ciphers.substitution.monoalphabetic import CaesarShiftCipher
# from ciphers import AtbashCipher
# from ciphers import *
#
#
# x = list(range(1, 20))
# print(x)
# y = [3, 5, 8]
# print(y)
#
# def u(x):
#     seen = set()
#     o = type(x)()
#     for n in x:
#         if n not in seen:
#             seen.add(n)
#             o += n
#     return o
#
#
# def q(x, y):
#     z = y[:]
#     for n in x:
#         if n not in y:
#             z += n
#     # z = y + [n for n in x if n not in y]
#     return z
#
# x='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# y='KANGAROO'
# # z = u([2,4,5,2,5,6])
# z = q(x, y)
# print(z)
#
cipher = CaesarShiftCipher()
# # cipher = AtbashCipher()
# cipher = KeywordCipher(keyword='KANGAROO')
y = cipher.encode('HELLO, WORLD')
# # y = cipher.encode('HELLO, WORLD')
print(y)
