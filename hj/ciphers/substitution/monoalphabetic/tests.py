#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from . import *  # noqa
import string


class CipherTest(unittest.TestCase):

    MESSAGE_PLAIN = 'HELLO, WORLD!'
    MESSAGE_STRICT = 'HELLOWORLD'
    PASSPHRASE = 'OCEANOGRAPHYWHAT'

    def _transcode(self, cipher, msg, msg_strict, msg_enc_expected, strict):
        encoded = cipher.encode(msg, strict=strict)
        # [TODO] should we test with both strict and non-strict decoding?
        decoded = cipher.decode(encoded, strict=strict)

        self.assertEqual(encoded, msg_enc_expected)
        if msg_enc_expected is not '':
            self.assertNotEqual(encoded, decoded)
            self.assertEqual(decoded, strict and msg_strict or msg)

    def _transcode_reverse(self, cipher, msg, msg_strict, msg_enc_expected,
                           strict):
        encoded = cipher.decode(msg, strict=strict)
        # [TODO] should we test with both strict and non-strict decoding?
        decoded = cipher.encode(encoded, strict=strict)

        self.assertEqual(encoded, msg_enc_expected)
        if msg_enc_expected is not '':
            self.assertNotEqual(encoded, decoded)
            self.assertEqual(decoded, strict and msg_strict or msg)

    def test_atbashcipher(self):
        c = AtbashCipher()
        self._transcode(c, self.MESSAGE_PLAIN, None, 'SVOOL, DLIOW!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'SVOOLDLIOW', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'SVOOL, DLIOW!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'SVOOLDLIOW', strict=True)

    def test_caesarcipher(self):
        c = CaesarCipher()
        self._transcode(c, self.MESSAGE_PLAIN, None, 'KHOOR, ZRUOG!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'KHOORZRUOG', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'EBIIL, TLOIA!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'EBIILTLOIA', strict=True)

    def test_shiftcipher(self):
        c = ShiftCipher(17)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'YVCCF, NFICU!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'YVCCFNFICU', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'QNUUX, FXAUM!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'QNUUXFXAUM', strict=True)

    def test_keywordcipher(self):
        c = KeywordCipher(keyword='KANGAROO')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'CRHHL, WLQHG!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'CRHHLWLQHG', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'LJOOF, WFEOI!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'LJOOFWFEOI', strict=True)

    def test_affinecipher(self):
        c = AffineCipher(7, 3)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'AFCCX, BXSCY!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'AFCCXBXSCY', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'IPQQJ, ZJCQA!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'IPQQJZJCQA', strict=True)


if __name__ == '__main__':
    unittest.main()
