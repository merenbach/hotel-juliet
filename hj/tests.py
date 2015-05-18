#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ciphers import *

# class AlphabetTest(unittest.TestCase):
#     def test_rotate(self):
#         ab = Alphabet()
#         for i in range(0, len(ab)):
#             rot_left = ab.rotated(i)
#             rot_right = ab.rotated(-i)


class CipherTest(unittest.TestCase):

    MESSAGE_PLAIN = 'HELLO, WORLD!'
    MESSAGE_STRICT = 'HELLOWORLD'
    PASSPHRASE = 'OCEANOGRAPHYWHAT'

    def _transcode(self, cipher, msg, msg_strict, msg_enc, strict):
        encoded = cipher.encode(msg, strict=strict)
        # [TODO] should we test with both strict and non-strict decoding?
        decoded = cipher.decode(encoded, strict=strict)

        self.assertEqual(encoded, msg_enc)
        self.assertEqual(decoded, strict and msg_strict or msg)

    def _transcode_reverse(self, cipher, msg, msg_strict, msg_enc, strict):
        encoded = cipher.decode(msg, strict=strict)
        # [TODO] should we test with both strict and non-strict decoding?
        decoded = cipher.encode(encoded, strict=strict)

        self.assertEqual(encoded, msg_enc)
        self.assertEqual(decoded, strict and msg_strict or msg)


    def test_caesarcipher(self):
        c = CaesarCipher()
        self._transcode(c, self.MESSAGE_PLAIN, None, 'KHOOR, ZRUOG!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'KHOORZRUOG', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'EBIIL, TLOIA!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'EBIILTLOIA', strict=True)

    def test_atbashcipher(self):
        c = AtbashCipher()
        self._transcode(c, self.MESSAGE_PLAIN, None, 'SVOOL, DLIOW!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'SVOOLDLIOW', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'SVOOL, DLIOW!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'SVOOLDLIOW', strict=True)

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


    def test_vigenere(self):
        c = VigenereCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, KUILS!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBKUILS', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, IIALO!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBIIALO', strict=True)

    def test_variantbeaufort(self):
        c = VariantBeaufortCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'TCHLB, IIALO!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBIIALO', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'VGPLB, KUILS!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBKUILS', strict=True)

    def test_trithemius(self):
        c = TrithemiusCipher()
        self._transcode(c, self.MESSAGE_PLAIN, None, 'HFNOS, BUYTM!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'HFNOSBUYTM', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'HDJIK, RIKDU!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'HDJIKRIKDU', strict=True)

    def test_beaufort(self):
        c = BeaufortCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'HYTPZ, SSAPM!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'HYTPZSSAPM', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'HYTPZ, SSAPM!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'HYTPZSSAPM', strict=True)

    def test_gronsfeld(self):
        c = GronsfeldCipher('23132')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'JHMOQ, YRSOF!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'JHMOQYRSOF', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'FBKIM, ULQIB!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'FBKIMULQIB', strict=True)

    def test_porta(self):
        c = PortaCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'OSNYI, CLJYX!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'OSNYICLJYX', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'OSNYI, CLJYX!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'OSNYICLJYX', strict=True)

if __name__ == '__main__':
    unittest.main()
