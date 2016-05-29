#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ciphers import *
from utils import *
import string
import itertools

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

    def testLCG(self):
        # [TODO] expand these tests

        #
        # Various sequences figures borrowed for verification from:
        #
        # <https://www.mi.fu-berlin.de/inf/groups/ag-tech/teaching/2012_SS/
        #  L_19540_Modeling_and_Performance_Analysis_with_Simulation/06.pdf>
        #

        g = lcg(100, 17, 43, 27, hull_dobell=False)
        g_expected = [27, 2, 77, 52, 27]
        self.assertEqual(list(itertools.islice(g, 5)), g_expected)

        g = lcg(64, 13, 0, 1, hull_dobell=False)
        g_expected = [1, 13, 41, 21, 17, 29, 57, 37, 33, 45, 9, 53, 49, 61, 25,
                      5, 1]
        self.assertEqual(list(itertools.islice(g, 17)), g_expected)

        g = lcg(64, 13, 0, 2, hull_dobell=False)
        g_expected = [2, 26, 18, 42, 34, 58, 50, 10, 2]
        self.assertEqual(list(itertools.islice(g, 9)), g_expected)

        g = lcg(64, 13, 0, 3, hull_dobell=False)
        g_expected = [3, 39, 59, 63, 51, 23, 43, 47, 35, 7, 27, 31, 19, 55, 11,
                      15, 3]
        self.assertEqual(list(itertools.islice(g, 17)), g_expected)

        g = lcg(64, 13, 0, 4, hull_dobell=False)
        g_expected = [4, 52, 36, 20, 4]
        self.assertEqual(list(itertools.islice(g, 5)), g_expected)


    def testUpwardRound(self):
        # [TODO] expand these tests

        tests = [
            (1, 1, 1),
            (1, 2, 2),
            (2, 1, 2),
            (3, 10, 12),
            (4, 10, 12),
            (5, 10, 10),
            (6, 10, 12),
            (7, 10, 14),
            (8, 9, 16),
            (8, 8, 8),
        ]
        for factor, base, expected in tests:
            out = upward_factor(factor, base)
            self.assertEqual(out, expected)

        with self.assertRaises(ZeroDivisionError):
            upward_factor(0, 0)

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
