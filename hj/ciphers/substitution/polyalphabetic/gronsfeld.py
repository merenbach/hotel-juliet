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
    Technically, it can be made totally symmetric if a Beaufort tabula recta
    is used instead.

    """
    def __init__(self, passphrase, charset=None):
        super().__init__(passphrase, charset=charset)

    def _make_tableau(self, charset):
        """ Same alphabet as normal, with digits for keys.

        """
        return TabulaRecta(charset, keys=digits)
