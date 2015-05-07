# -*- coding: utf-8 -*-

from . import VigenereCipher


class VariantBeaufortCipher(VigenereCipher):
    """ Vigenere cipher with encoding and decoding steps reversed """

    def generate_cipher_func(self, reverse):
        """ Convert characters from one alphabet to another (reverse is reversed [sic]) """
        super().generate_cipher_func(not reverse)
