#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import VigenereCipher
from string import digits
from utils.alphabet import Alphabet
from utils.tabula_recta import TabulaRecta


class GronsfeldCipher(VigenereCipher):
    def __init__(self, tabula_recta=None, passphrase=None):
        if not tabula_recta:
            tabula_recta = TabulaRecta(Alphabet(), Alphabet(digits))
        super().__init__(tabula_recta, passphrase, autoclave=False)
