#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from string import digits
from utils import TabulaRecta


class GronsfeldCipher(VigenereCipher):
    """ Vigenere with only ten key alphabets, corresponding to 0 through 9.

    Parameters
    ----------
    countersign : str
        An encryption/decryption key.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    Since the countersign is numeric, autoclave makes somewhat less sense here.
    [TODO] Technically, it can be made totally symmetric if a Beaufort tabula recta is used instead.

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
        return TabulaRecta(alphabet, keys=digits)
