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
    def _encode(self, s, block):
        """ Reverse the encoding direction.

        """
        return super()._decode(s, block)

    def _decode(self, s, block):
        """ Reverse the decoding direction.

        """
        return super()._encode(s, block)
