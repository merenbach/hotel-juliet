#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import *

class CaesarShiftCipher(MonoSubCipher):
    ### Monoalphabetic cipher to shift letters
    def __init__(self, alphabet=None, shift=3):
        if not alphabet:
            alphabet = Alphabet()
        transformed = alphabet << shift
        super(CaesarShiftCipher, self).__init__(alphabet, transformed)
