#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import VigenereCipher
from string import digits
from utils.alphabet import Alphabet
from utils.tabula_recta import TabulaRecta


class GronsfeldCipher(VigenereCipher):
    def __init__(self, alphabet=None, passphrase=None):
        tabula_recta = TabulaRecta(alphabet, alphabet_=Alphabet(digits))
        super().__init__(passphrase, tabula_recta=tabula_recta, autoclave=False)
