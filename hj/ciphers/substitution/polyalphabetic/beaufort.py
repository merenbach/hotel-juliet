#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import PolySubCipher


class BeaufortCipher(PolySubCipher):
    """ Beaufort cipher.  Symmetric.  Not to be confused with Variant Beaufort.

    Notes
    -----
    Autoclave makes no sense for this cipher, as far as I can tell, so it is
    forced to `False`.

    """
    def __init__(self, passphrase, alphabet=None):
        super().__init__(passphrase, alphabet=alphabet, autoclave=False)

    def _cipher(self, msg_char, key_char, reverse=False):
        """ Convert characters from one alphabet to another (reverse is ignored) """
        return self.tabula_recta.decode(key_char, msg_char)
