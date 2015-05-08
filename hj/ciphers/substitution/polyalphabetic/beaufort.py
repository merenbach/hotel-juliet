#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import PolySubCipher
from utils.tabula_recta import TabulaRecta


class BeaufortCipher(PolySubCipher):
    def __init__(self, tabula_recta=None, passphrase=None):
        if not tabula_recta:
            tabula_recta = TabulaRecta()
        super().__init__(tabula_recta, passphrase, autoclave=False)

    def generate_cipher_func(self, reverse):
        """ Convert characters from one alphabet to another (reverse is ignored) """
        return lambda msg_char, key_char : self.tabula_recta.locate(key_char, msg_char)

    def _transcode(self, s, strict=False, reverse=False):
        """ Convert characters from one alphabet to another (reverse is ignored) """
        return super()._transcode(s, strict=strict, reverse=False)
