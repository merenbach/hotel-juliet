#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from .vigenere import VigenereCipher
from utils import PortaTabulaRecta


class PortaCipher(VigenereCipher):
    """ Della porta cipher.  Symmetric.

    Notes
    -----
    This is a variant of the Beaufort cipher, not to be confused with the
    "variant Beaufort" cipher, which is a variant of the Vigenere.

    [TODO] ensure alphabet length is divisible by the number of items in each
    group in the leftmost (key) column
    [TODO] does/should this support autoclave?

    """
    # def __init__(self, passphrase, alphabet=None, autoclave=False):
    #     tableau = PortaTabulaRecta(alphabet)
    #     super().__init__(passphrase, tableau=tableau, autoclave=autoclave)

    def _make_tableau(self, alphabet):
        """ Same alphabet as normal, with digits for keys.

        """
        return PortaTabulaRecta(alphabet=alphabet)
