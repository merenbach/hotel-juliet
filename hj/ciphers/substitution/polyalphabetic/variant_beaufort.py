#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import TabulaRecta


class VariantBeaufortCipher(VigenereCipher):
    """ Simply the Vigenère cipher with encoding and decoding steps reversed.

    Notes
    -----
    Unlike the Vigenère cipher, the _plaintext_ letters are located inside the
    grid.  Thus encryption simply swaps the location of the plaintext and
    ciphertext characters, versus the Vigenère.

    Although such an implementation works just fine, a separate tabula recta is
    sometimes employed to tailor Vigenère cipher techniques to this cipher.
    In an effort to reduce code duplication (and to make a cool tabula recta
    display), that alternative tableau is used here.

    Not to be confused with the true (symmetric) Beaufort cipher, which also
    uses the tabula recta.

    """
    @staticmethod
    def maketableau(alphabet):
        """ Create a tabula recta for transcoding.

        Parameters
        ----------
        alphabet : str
            A character set to use for transcoding.

        Returns
        -------
        out : utils.tableau.TabulaRecta
            A tabula recta to use for transcoding.

        """
        return TabulaRecta(alphabet[::-1], ct=alphabet[::-1], keys=alphabet)
