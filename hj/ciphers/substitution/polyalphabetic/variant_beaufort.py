#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher


class VariantBeaufortCipher(VigenereCipher):
    """ Vigenere cipher with encoding and decoding steps reversed.

    Notes
    -----
    Not to be confused with the (symmetric) Beaufort cipher, which also uses
    the tabula recta.

    """
    def _encode(self, s):
        """ Reverse the encoding direction.

        Notes
        -----
        This needs to be done currently with `_decode`, rather than `decode`,
        because it's still an encryption operation and we just want to change
        the internals.

        """
        return super()._decode(s)

    def _decode(self, s):
        """ Reverse the decoding direction.

        Notes
        -----
        This needs to be done currently with `_encode`, rather than `encode`,
        because it's still a decryption operation and we just want to change
        the internals.

        """
        return super()._encode(s)
