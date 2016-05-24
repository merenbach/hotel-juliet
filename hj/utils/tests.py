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

    def testCoprimality(self):
        # [TODO] expand these tests

        yes = [(3, 5), (7, 20), (14, 15), (172, 17)]
        no = [(2, 4), (2, 22), (3, 15), (14, 28)]

        for a, b in yes:
            self.assertEqual(True, coprime(a, b))
            self.assertEqual(True, coprime(b, a))
        for a, b in no:
            self.assertEqual(False, coprime(a, b))
            self.assertEqual(False, coprime(b, a))

    def testDivisibility(self):
        # [TODO] expand these tests

        yes = [(100, 100), (100, 10), (24, 3), (24, 8)]
        no = [(10, 100), (24, 7), (3, 24), (8, 7)]

        for a, b in yes:
            self.assertEqual(True, divisible(a, b))

        for a, b in no:
            self.assertEqual(False, divisible(a, b))

    def testRegularity(self):
        # [TODO] expand these tests

        yes = [(98, 168), (24, 6), (6, 24), (12, 18), (3, 0), (1, 1)]
        no = [(168, 98), (168, 132), (132, 168), (2, 1)]

        for a, b in yes:
            self.assertEqual(True, regular(a, b))

        for a, b in no:
            self.assertEqual(False, regular(a, b))

        with self.assertRaises(ValueError):
            regular(0, 0)

    def testUnique(self):
        io_vals = [
                ('', 'KANGAROO', ''),
                ('KANGAROO', '', 'KANGRO'),
                ('KANGAROO', 'KANGAROO', 'KANGRO'),
                ('KANGAROO', '31337h#xorz', 'KANGRO'),
                ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'KANGAROO',
                    'KANGROBCDEFHIJLMPQSTUVWXYZ'),
                ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'OCEANOGRAPHYWHAT',
                    'OCEANGRPHYWTBDFIJKLMQSUVXZ'),
        ]

        for src, pre, dst in io_vals:
            out = ''.join(unique(src, prefix=pre))
            self.assertEqual(out, dst)

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
