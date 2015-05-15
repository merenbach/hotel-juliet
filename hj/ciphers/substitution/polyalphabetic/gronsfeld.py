#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import VigenereCipher
from string import digits
from utils.alphabet import Alphabet, AlphabetTranscoder
from utils.tabula_recta import TabulaRecta


class GronsfeldCipher(VigenereCipher):
    def __init__(self, passphrase, alphabet=None):
        alphabet = Alphabet(alphabet)
        super().__init__(passphrase, autoclave=False)
        self.tcoder = AlphabetTranscoder(alphabet[:len(digits)], digits)

    def _cipher(self, msg_char, key_char, reverse=False):
        key_char = self.tcoder.decode(key_char)
        return super()._cipher(msg_char, key_char, reverse=reverse)
