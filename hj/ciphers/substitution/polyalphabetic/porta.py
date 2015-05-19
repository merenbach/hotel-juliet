#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import PortaTabulaRecta


class PortaCipher(VigenereCipher):
    """ Della porta cipher.  Symmetric.

    Notes
    -----
    This is similar to the Beaufort cipher, not to be confused with the
    "variant Beaufort" cipher, which is a variant of the Vigenere.

    [TODO] ensure alphabet length is divisible by the number of items in each
    group in the leftmost (key) column

    Since this is a symmetric cipher, autoclave is not implemented.

    """
    def __init__(self, passphrase, alphabet=None):
        super().__init__(passphrase, alphabet=alphabet)

    def _make_tableau(self, alphabet):
        """ Same alphabet as normal, with digits for keys.

        """
        return PortaTabulaRecta(alphabet=alphabet)
