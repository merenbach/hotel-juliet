#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from string import digits


class GronsfeldCipher(VigenereCipher):
    """ Vigenere but with only ten key alphabets, corresponding to 0..9.

    """
    def _make_alphabets(self, alphabet, key_alphabet=None):
        return super()._make_alphabets(alphabet, key_alphabet=digits)
