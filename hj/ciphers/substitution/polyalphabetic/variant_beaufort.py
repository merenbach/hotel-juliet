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
    def _encode(self, *args, **kwargs):
        """ Reverse the encoding direction.

        """
        return super()._decode(*args, **kwargs)

    def _decode(self, *args, **kwargs):
        """ Reverse the decoding direction.

        """
        return super()._encode(*args, **kwargs)
