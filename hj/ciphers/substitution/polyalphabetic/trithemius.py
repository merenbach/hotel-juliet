# -*- coding: utf-8 -*-

from . import VigenereCipher
from utils.tabula_recta import TabulaRecta


class TrithemiusCipher(VigenereCipher):
    def __init__(self, tabula_recta=None):
        if not tabula_recta:
            tabula_recta = TabulaRecta()
        passphrase = tabula_recta.key_alphabet
        super().__init__(tabula_recta, passphrase, autoclave=False)
