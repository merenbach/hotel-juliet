#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import TabulaRecta


class BeaufortCipher(VigenereCipher):
    """ Beaufort cipher.  Symmetric.  Not to be confused with Variant Beaufort.

    Notes
    -----
    Autoclave makes no sense for this cipher, as far as I can tell, so it is
    forced to `False`.

    Unlike the vigenere cipher, the *key* letter is located inside the grid;
    put another way, the `cipher` method in the parent class simply has its
    `key_char` and `msg_char` arguments swapped.  Although this implementation
    works just fine, a separate tabula recta is often described online
    to make the Vigenere cipher encode just like the Beaufort.

    To reduce code duplication, that tableau is used here.

    """
    def __init__(self, passphrase, alphabet=None):
        super().__init__(passphrase, alphabet=alphabet, autoclave=False)

    def _make_tableau(self, alphabet):
        """ Same alphabet as normal, with digits for keys.

        """
        return TabulaRecta(alphabet=alphabet, keys=alphabet[::-1],
                msg_alphabet=alphabet[::-1])
