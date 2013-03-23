#!/usr/bin/python
# -*- coding: utf-8 -*-

from ciphers.substitution.monoalphabetic import MonoSubCipher
from utils.alphabet import *

class AtbashCipher(MonoSubCipher):
    def __init__(self, alphabet=None, processor=None):
        if not alphabet:
            alphabet = Alphabet()
        transformed = alphabet.reversed()
        super(AtbashCipher, self).__init__(alphabet, transformed)
