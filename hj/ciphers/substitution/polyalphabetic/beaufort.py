#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import TabulaRecta


class BeaufortCipher(VigenereCipher):
    """ The symmetric, "true" (as opposed to "variant") Beaufort cipher.

    Notes
    -----
    Unlike the Vigenère cipher, the _key_ letter is located inside the grid.
    Thus encryption simply swaps the location of the message character and
    the key character in encryption and decryption, versus the Vigenère.

    Although such an implementation works just fine, a separate tabula recta is
    sometimes employed to tailor Vigenère cipher techniques to this cipher.
    In an effort to reduce code duplication (and to make a cool tabula recta
    display), that alternative tableau is used here.

    Not to be confused with the variant Beaufort cipher, which also
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

        Notes
        -----
        Since this is invoked by `__init__()` before instance is totally
        initialized, please don't perform any operations that expect a fully
        constructed instance.

        """
        return TabulaRecta(alphabet, ct=alphabet[::-1], keys=alphabet[::-1])
