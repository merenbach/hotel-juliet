#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import PolySubCipher
from utils.tabula_recta import TabulaRecta


class BeaufortCipher(PolySubCipher):
    """ Beaufort cipher.  Symmetric.  Not to be confused with Variant Beaufort.

    Notes
    -----
    Autoclave makes no sense for this cipher, as far as I can tell, so it is
    forced to `False`.

    """
    def __init__(self, passphrase, tabula_recta=None):
        super().__init__(passphrase,
                         tabula_recta=tabula_recta,
                         autoclave=False)

    def generate_cipher_func(self, reverse):
        """ Convert characters from one alphabet to another (reverse is ignored) """
        return lambda msg_char, key_char : self.tabula_recta.locate(key_char, msg_char)

    def _transcode(self, s, strict=False, reverse=False):
        """ Convert characters from one alphabet to another (reverse is ignored) """
        return super()._transcode(s, strict=strict, reverse=False)
