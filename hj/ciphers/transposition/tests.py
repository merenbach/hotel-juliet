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

    def test_scytale(self):
        c = ScytaleCipher(4)
        self._transcode(c, self.MESSAGE_PLAIN, None, 'HOO!E,RXL LXLWDX', strict=False)
        # self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'HOOERXLLXLWDX', strict=True)
        # self._transcode(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'VGPLBKUILS', strict=True)
        # self._transcode_reverse(c, self.MESSAGE_PLAIN, None, 'TCHLB, IIALO!', strict=False)
        # self._transcode_reverse(c, self.MESSAGE_PLAIN, self.MESSAGE_STRICT, 'TCHLBIIALO', strict=True)


if __name__ == '__main__':
    unittest.main()
