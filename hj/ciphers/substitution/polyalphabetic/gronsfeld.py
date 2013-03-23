#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import VigenereCipher
from utils.tabula_recta import *

class GronsfeldCipher(VigenereCipher):
    def __init__(self, tabula_recta=None, passphrase=None):
        if not tabula_recta:
            from string import digits
            tabula_recta = TabulaRecta(Alphabet(), Alphabet(digits))
        super(GronsfeldCipher, self).__init__(tabula_recta, passphrase, autoclave=False)
