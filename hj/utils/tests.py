#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ciphers import *
from utils import *
import string

# class AlphabetTest(unittest.TestCase):
#     def test_rotate(self):
#         ab = Alphabet()
#         for i in range(0, len(ab)):
#             rot_left = ab.rotated(i)
#             rot_right = ab.rotated(-i)


class UtilsTest(unittest.TestCase):

    PASSPHRASE = 'OCEANOGRAPHYWHAT'

    def testLeftRotation(self):
        s = 'HELLO, WORLD!'
        expected_out = [
            'HELLO, WORLD!',
            'ELLO, WORLD!H',
            'LLO, WORLD!HE',
            'LO, WORLD!HEL',
            'O, WORLD!HELL',
            ', WORLD!HELLO',
            ' WORLD!HELLO,',
            'WORLD!HELLO, ',
            'ORLD!HELLO, W',
            'RLD!HELLO, WO',
            'LD!HELLO, WOR',
            'D!HELLO, WORL',
            '!HELLO, WORLD',
        ]
        s_len = len(s)
        out = [lrotated(s, i) for i in range(s_len)]
        self.assertEqual(expected_out, out)

        out = [lrotated(s, i + s_len) for i in range(s_len)]
        self.assertEqual(expected_out, out)

        out = [lrotated(s, i - s_len) for i in range(s_len)]
        self.assertEqual(expected_out, out)

    def testExtendableIterator(self):
        iterator = extendable_iterator('')
        self.assertEqual(''.join(iterator), '')

        iterator = extendable_iterator(self.PASSPHRASE)
        self.assertEqual(''.join(iterator), self.PASSPHRASE)

        out = []
        iterator = extendable_iterator(self.PASSPHRASE[0:2])
        out.append(next(iterator))
        out.append(iterator.send(self.PASSPHRASE[2]))
        out.append(next(iterator))
        out.append(iterator.send([self.PASSPHRASE]))

        self.assertEqual(out, ['O', 'C', 'E', self.PASSPHRASE])

    # def testEqualLengthZip(self):
    #     a = string.ascii_uppercase
    #     b = string.ascii_lowercase
    #     c = 'another string w/length 26'
    #     d = 'a string of some other length'
    #
    #     self.assertEqual(list(ezip(a, a)), list(zip(a, a)))
    #     self.assertEqual(list(ezip(a, b)), list(zip(a, b)))
    #     self.assertEqual(list(ezip(a, c, c)), list(zip(a, c, c)))
    #     self.assertEqual(list(ezip(a, b, c)), list(zip(a, b, c)))
    #
    #     # test raising of ValueError with unequal alphabets
    #     with self.assertRaises(ValueError):
    #         MonoSubCipher(a, c)
    #
    #     with self.assertRaises(ValueError):
    #         MonoSubCipher(c, d)
    #
    #     with self.assertRaises(ValueError):
    #         ezip(c, d)
    #
    #     with self.assertRaises(ValueError):
    #         ezip(a, b, c, d)


if __name__ == '__main__':
    unittest.main()
