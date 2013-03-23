#!/usr/bin/python
# -*- coding: utf-8 -*-

from ciphers.substitution.polyalphabetic import PolySubCipher
from utils.tabula_recta import *

class VigenereCipher(PolySubCipher):
    def __init__(self, tabula_recta=None, passphrase=None, autoclave=False):
        if not tabula_recta:
            tabula_recta = TabulaRecta()
        super(VigenereCipher, self).__init__(tabula_recta, passphrase, autoclave=autoclave)

    def generate_cipher_func(self, reverse):
        """ Convert characters from one alphabet to another """
        if not reverse:
            return lambda msg_char, key_char : self.tabula_recta.intersect(msg_char, key_char)
        else:
            return lambda msg_char, key_char : self.tabula_recta.locate(msg_char, key_char)
