#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import VigenereCipher


class VariantBeaufortCipher(VigenereCipher):
    """ Vigenere cipher with encoding and decoding steps reversed """

    def _cipher(self, msg_char, key_char, reverse=False):
        return super()._cipher(msg_char, key_char, not reverse)
