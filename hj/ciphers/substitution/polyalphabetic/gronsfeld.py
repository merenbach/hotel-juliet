#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from string import digits
from utils import TabulaRecta


class GronsfeldCipher(VigenereCipher):
    """ Vigenere with only ten key alphabets, corresponding to 0..9.

    Parameters
    ----------
    passphrase : str
        An encryption/decryption key.
    charset : str, optional
        A character set to use for transcoding.  Default `None`.

    Notes
    -----
    Since the passphrase is numeric, autoclave makes less sense here.

    [TODO] raise valueerror when passphrase contains non digits?

    """
    def __init__(self, passphrase, charset=None):
        super().__init__(passphrase, charset=charset)

    def _make_tableau(self, alphabet):
        """ Same alphabet as normal, with digits for keys.

        """
        return TabulaRecta(alphabet=alphabet, keys=digits)
