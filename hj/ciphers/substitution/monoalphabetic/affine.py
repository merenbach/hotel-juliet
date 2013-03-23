#!/usr/bin/python
# -*- coding: utf-8 -*-

from ciphers.substitution.monoalphabetic import MonoSubCipher
from utils.alphabet import *

class AffineCipher(MonoSubCipher):
    def __init__(self, alphabet, m, b):
        """ multiply mx + b """
        # We're cheating here by not actually having the decryption method use the "inverse" argument
        transformed = alphabet.affinal(m, b)
        super(AffineCipher, self).__init__(alphabet, transformed)
