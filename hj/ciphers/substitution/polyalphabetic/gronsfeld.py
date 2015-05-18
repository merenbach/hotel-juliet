#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from string import digits


class GronsfeldCipher(VigenereCipher):
    """ Vigenere but with only ten key alphabets, corresponding to 0..9.

    """
    def __init__(self, passphrase, alphabet=None):
        super().__init__(passphrase, alphabet=alphabet, key_alphabet=digits,
                         autoclave=False)
