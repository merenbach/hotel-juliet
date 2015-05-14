#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import PolySubCipher
from utils.tabula_recta import TabulaRecta


class VigenereCipher(PolySubCipher):
    """ THE Vigenere cipher, conceptual foundation of many other ciphers.

    """
    def __init__(self, passphrase, tabula_recta=None, autoclave=False):
        super().__init__(passphrase,
                         tabula_recta=tabula_recta,
                         autoclave=autoclave)

    def generate_cipher_func(self, reverse):
        """ Convert characters from one alphabet to another """
        if not reverse:
            return lambda msg_char, key_char : self.tabula_recta.intersect(msg_char, key_char)
        else:
            return lambda msg_char, key_char : self.tabula_recta.locate(msg_char, key_char)
