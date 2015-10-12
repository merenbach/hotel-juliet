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
    verbose_name = 'Variant Beaufort'

    def _encode(self, s):
        """ Reverse the encoding direction.

        """
        return super()._decode(s)

    def _decode(self, s):
        """ Reverse the decoding direction.

        """
        return super()._encode(s)
