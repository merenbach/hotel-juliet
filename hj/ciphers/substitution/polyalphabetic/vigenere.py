#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import PolySubCipher


class VigenereCipher(PolySubCipher):
    """ THE Vigenere cipher, conceptual foundation of many other ciphers.

    """
    def __init__(self, passphrase, alphabet=None, autoclave=False):
        super().__init__(passphrase, alphabet=alphabet, autoclave=autoclave)

    def _cipher(self, msg_char, key_char, reverse=False):
        """ Convert characters from one alphabet to another """
        return self.tabula_recta.transcode(msg_char, key_char,
                                           intersect=not reverse)
