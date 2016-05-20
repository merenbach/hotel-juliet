#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from . import *  # noqa
import string


class CipherTest(unittest.TestCase):

    MESSAGE_PLAIN = 'HELLO, WORLD!'
    MESSAGE_STRICT = 'HELLOWORLD'
    PASSPHRASE = 'OCEANOGRAPHYWHAT'

    def _transcode(self, cipher, msg, msg_strict, msg_enc_expected, block):
        encoded = cipher.encode(msg, block=block)
        # [TODO] should we test with both strict and non-strict decoding?
        decoded = cipher.decode(encoded, block=block)

        self.assertEqual(encoded, msg_enc_expected)
        if msg_enc_expected is not '':
            self.assertNotEqual(encoded, decoded)
            self.assertEqual(decoded, block==0 and msg_strict or msg)

    def _transcode_reverse(self, cipher, msg, msg_strict, msg_enc_expected,
                           block):
        encoded = cipher.decode(msg, block=block)
        # [TODO] should we test with both strict and non-strict decoding?
        decoded = cipher.encode(encoded, block=block)

        self.assertEqual(encoded, msg_enc_expected)
        if msg_enc_expected is not '':
            self.assertNotEqual(encoded, decoded)
            self.assertEqual(decoded, block==0 and msg_strict or msg)

    def test_atbashcipher(self):
        c = AtbashCipher()
        self._transcode(c, self.MESSAGE_PLAIN, None, 'SVOOL, DLIOW!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'SVOOLDLIOW', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'SVOOL, DLIOW!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'SVOOLDLIOW', block=0)

    def test_caesarcipher(self):
        c = CaesarCipher()
        self._transcode(c, self.MESSAGE_PLAIN, None, 'KHOOR, ZRUOG!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'KHOORZRUOG', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'EBIIL, TLOIA!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'EBIILTLOIA', block=0)

        c = CaesarCipher(17)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'YVCCF, NFICU!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'YVCCFNFICU', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'QNUUX, FXAUM!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'QNUUXFXAUM', block=0)

    def test_keywordcipher(self):
        c = KeywordCipher('KANGAROO')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'CRHHL, WLQHG!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'CRHHLWLQHG', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'LJOOF, WFEOI!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'LJOOFWFEOI', block=0)

    def test_affinecipher(self):
        c = AffineCipher(7, 3)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'AFCCX, BXSCY!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'AFCCXBXSCY', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'IPQQJ, ZJCQA!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'IPQQJZJCQA', block=0)

    def test_decimationcipher(self):
        c = DecimationCipher(7)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'XCZZU, YUPZV!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'XCZZUYUPZV', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'BIJJC, SCVJT!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'BIJJCSCVJT', block=0)


if __name__ == '__main__':
    unittest.main()
