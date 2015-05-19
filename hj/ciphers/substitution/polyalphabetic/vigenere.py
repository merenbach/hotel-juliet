#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher


class VigenereCipher(PolySubCipher):
    """ THE Vigenere cipher, conceptual foundation of several other ciphers.

    """
    def _cipher(self, msg_char, key_char, reverse):
        """ Convert characters from one alphabet to another

        """
        if not reverse:
            cipher_func = self.tabula_recta.encode
        else:
            cipher_func = self.tabula_recta.decode
        return cipher_func(msg_char, key_char)
