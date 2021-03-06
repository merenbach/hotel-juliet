#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import TabulaRecta
import string


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
        return TabulaRecta(alphabet, keys=string.digits)
