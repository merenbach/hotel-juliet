#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import PolySubCipher


class VigenereCipher(PolySubCipher):
    """ THE Vigenere cipher, conceptual foundation of several other ciphers.

    """
    def __init__(self, passphrase, alphabet=None, autoclave=False):
        super().__init__(passphrase, alphabet=alphabet, autoclave=autoclave)

    def _cipher(self, msg_char, key_char, reverse=False):
        """ Convert characters from one alphabet to another """
        if reverse:
            return self.tabula_recta.decode(msg_char, key_char)
        else:
            return self.tabula_recta.encode(msg_char, key_char)
