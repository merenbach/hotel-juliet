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

    def test_vigenere(self):
        c = VigenereCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, KUILS!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBKUILS', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, IIALO!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBIIALO', strict=True)

        c = VigenereCipher('8O3CEiAN#OGRAPHYrrWrrHATz')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, KUILS!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBKUILS', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, IIALO!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBIIALO', strict=True)

        with self.assertRaises(ValueError):
            VigenereCipher('b4dk3y')
            VigenereCipher('')

    def test_vigenere_text_autoclave(self):
        c = VigenereTextAutoclaveCipher(self.PASSPHRASE[:5])
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, DSCWR!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBDSCWR', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, DMKAC!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBDMKAC', strict=True)

        c = VigenereTextAutoclaveCipher('9OC33EarqAN!')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, DSCWR!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBDSCWR', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, DMKAC!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBDMKAC', strict=True)

        with self.assertRaises(ValueError):
            VigenereTextAutoclaveCipher('b4dk3y')
            VigenereTextAutoclaveCipher('')

    def test_vigenere_key_autoclave(self):
        c = VigenereKeyAutoclaveCipher(self.PASSPHRASE[:5])
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, RUGWE!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBRUGWE', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, PKGAP!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBPKGAP', strict=True)

        c = VigenereKeyAutoclaveCipher('9OC33EarqAN!')
        self._transcode(c, self.MESSAGE_PLAIN, None, 'VGPLB, RUGWE!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBRUGWE', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, PKGAP!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBPKGAP', strict=True)

        with self.assertRaises(ValueError):
            VigenereKeyAutoclaveCipher('b4dk3y')
            VigenereKeyAutoclaveCipher('')

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
        c = DellaPortaCipher(self.PASSPHRASE)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'OSNYI, CLJYX!', strict=False)
        self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'OSNYICLJYX', strict=True)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'OSNYI, CLJYX!', strict=False)
        self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'OSNYICLJYX', strict=True)


if __name__ == '__main__':
    unittest.main()
