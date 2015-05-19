#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from string import digits
from utils import GronsfeldTabulaRecta


class GronsfeldCipher(VigenereCipher):
    """ Vigenere with only ten key alphabets, corresponding to 0..9.

    Notes
    -----
    Since the passphrase is numeric, autoclave makes less sense here.

    [TODO] raise valueerror when passphrase contains non digits

    """
    TABULA_RECTA = GronsfeldTabulaRecta

    def __init__(self, passphrase, alphabet=None):
        super().__init__(passphrase, alphabet=alphabet, autoclave=False)
