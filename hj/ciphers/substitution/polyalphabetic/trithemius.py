#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import VigenereCipher
from utils.alphabet import Alphabet


class TrithemiusCipher(VigenereCipher):
    def __init__(self, alphabet=None):
        passphrase = Alphabet(alphabet)
        super().__init__(passphrase, alphabet=alphabet, autoclave=False)
