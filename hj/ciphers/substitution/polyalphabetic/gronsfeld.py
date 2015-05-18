#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from string import digits
from utils.alphabet import Alphabet


class GronsfeldCipher(VigenereCipher):
    def __init__(self, passphrase, alphabet=None):
        alphabet = Alphabet(alphabet)
        super().__init__(passphrase, autoclave=False)
        self._xtable = str.maketrans(digits, str(alphabet)[:len(digits)])

    def _cipher(self, msg_char, key_char, reverse=False):
        # [TODO] this allows non-numbers in key still... need to strip 'em!
        key_char = key_char.translate(self._xtable)
        return super()._cipher(msg_char, key_char, reverse=reverse)
