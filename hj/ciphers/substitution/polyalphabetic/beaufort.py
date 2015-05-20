#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import TabulaRecta


class BeaufortCipher(VigenereCipher):
    """ Beaufort cipher.  Symmetric.  Not to be confused with Variant Beaufort.

    Notes
    -----
    Unlike the vigenere cipher, the *key* letter is located inside the grid.
    Thus encryption simply swaps the location of the message character and
    the key character in encryption and decryption.

    Although such an implementation works just fine, a separate tabula recta is
    sometimes employed to tailor Vigenere cipher techniques to the Beaufort.
    In an effort to reduce code duplication (and to make a cool tabula recta
    display), that alternative tableau is used here.

    N.b.: Because this is a symmetric cipher, autoclave is disabled.

    """
    def __init__(self, passphrase, alphabet=None):
        super().__init__(passphrase, alphabet=alphabet)

    def _make_tableau(self, alphabet):
        """ Same alphabet as normal, with digits for keys.

        """
        ralphabet = alphabet.reverse()
        return TabulaRecta(alphabet=alphabet,
                           keys=ralphabet,
                           msg_alphabet=ralphabet)
