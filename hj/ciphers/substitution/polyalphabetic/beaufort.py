#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import TabulaRecta


class BeaufortCipher(VigenereCipher):
    """ Beaufort cipher.  Symmetric.  Not to be confused with Variant Beaufort.

    Parameters
    ----------
    countersign : str
        An encryption/decryption key.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    Unlike the vigenere cipher, the _key_ letter is located inside the grid.
    Thus encryption simply swaps the location of the message character and
    the key character in encryption and decryption.

    Although such an implementation works just fine, a separate tabula recta is
    sometimes employed to tailor Vigenere cipher techniques to the Beaufort.
    In an effort to reduce code duplication (and to make a cool tabula recta
    display), that alternative tableau is used here.

    N.b.: Because this is a symmetric cipher, autoclave is disabled.

    """
    def maketableau(self, alphabet):
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
