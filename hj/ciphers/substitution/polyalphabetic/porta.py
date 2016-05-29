#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils.tabula_recta import DellaPortaTabulaRecta


class DellaPortaCipher(VigenereCipher):
    """ Della porta cipher.  Symmetric.

    Parameters
    ----------
    countersign : str
        An encryption/decryption key.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    This is similar to the Beaufort cipher, not to be confused with the
    "variant Beaufort" cipher, which is a modified Vigenère.

    [TODO] ensure alphabet length is divisible by the number of items in each
    group in the leftmost (key) column

    Since this is a symmetric cipher, autoclave is not implemented.

    [TODO] Different algorithms appear to exist for this.  Understanding how
    this was implemented historically is a priority.

    [TODO] this is arguably not a variant of the Vigenere and should probably
    not inherit therefrom

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
        return DellaPortaTabulaRecta(alphabet)
