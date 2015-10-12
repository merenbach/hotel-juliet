#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils.tabula_recta import GronsfeldTabulaRecta


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
    Since the countersign is numeric, autoclave makes less sense here.
    [TODO] Technically, it can be made totally symmetric if a Beaufort tabula recta is used instead.

    """
    verbose_name = 'Gronsfeld'

    TABULA_RECTA = GronsfeldTabulaRecta

    def __init__(self, countersign, alphabet=None):
        super().__init__(countersign, alphabet=alphabet)
