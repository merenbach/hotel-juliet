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

    def test_vigenere(self):
        c = VigenereCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, KUILS!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBKUILS', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, IIALO!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBIIALO', block=0)

        c = VigenereCipher('8O3CEiAN#OGRAPHYrrWrrHATz')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, KUILS!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBKUILS', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, IIALO!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBIIALO', block=0)

        with self.assertRaises(ValueError):
            VigenereCipher('b4dk3y')
            VigenereCipher('')

    def test_vigenere_text_autoclave(self):
        c = VigenereTextAutoclaveCipher(self.PASSPHRASE[:5])
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, DSCWR!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBDSCWR', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, DMKAC!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBDMKAC', block=0)

        c = VigenereTextAutoclaveCipher('9OC33EarqAN!')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, DSCWR!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBDSCWR', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, DMKAC!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBDMKAC', block=0)

        with self.assertRaises(ValueError):
            VigenereTextAutoclaveCipher('b4dk3y')
            VigenereTextAutoclaveCipher('')

    def test_vigenere_key_autoclave(self):
        c = VigenereKeyAutoclaveCipher(self.PASSPHRASE[:5])
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, RUGWE!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBRUGWE', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, PKGAP!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBPKGAP', block=0)

        c = VigenereKeyAutoclaveCipher('9OC33EarqAN!')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, RUGWE!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBRUGWE', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, PKGAP!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBPKGAP', block=0)

        with self.assertRaises(ValueError):
            VigenereKeyAutoclaveCipher('b4dk3y')
            VigenereKeyAutoclaveCipher('')

    def test_variantbeaufort(self):
        c = VariantBeaufortCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'TCHLB, IIALO!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBIIALO', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'VGPLB, KUILS!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBKUILS', block=0)

    def test_trithemius(self):
        c = TrithemiusCipher()
        self._transcode(c, self.MESSAGE_PLAIN, None, 'HFNOS, BUYTM!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'HFNOSBUYTM', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'HDJIK, RIKDU!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'HDJIKRIKDU', block=0)

    def test_beaufort(self):
        c = BeaufortCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'HYTPZ, SSAPM!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'HYTPZSSAPM', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'HYTPZ, SSAPM!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'HYTPZSSAPM', block=0)

    def test_gronsfeld(self):
        c = GronsfeldCipher('23132')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'JHMOQ, YRSOF!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'JHMOQYRSOF', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'FBKIM, ULQIB!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'FBKIMULQIB', block=0)

    def test_porta(self):
        c = DellaPortaCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'OSNYI, CLJYX!', block=None)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'OSNYICLJYX', block=0)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'OSNYI, CLJYX!', block=None)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'OSNYICLJYX', block=0)


if __name__ == '__main__':
    unittest.main()
