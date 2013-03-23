#!/usr/bin/python
# -*- coding: utf-8 -*-

from ciphers.substitution.monoalphabetic import MonoSubCipher
from utils.alphabet import *

class KeywordCipher(MonoSubCipher):
    ### Monoalphabetic cipher to shift letters based on a keyword
    def __init__(self, alphabet=None, keyword=None):
        if not alphabet:
            alphabet = Alphabet()
        transformed = alphabet.keyed(keyword)
        super(KeywordCipher, self).__init__(alphabet, transformed)
