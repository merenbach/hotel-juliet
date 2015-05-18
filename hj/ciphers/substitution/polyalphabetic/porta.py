#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import PolySubCipher
from .beaufort import BeaufortCipher
from utils.base import grouper
from utils.alphabet import Alphabet
from utils import Transcoder


class PortaCipher(PolySubCipher):
    """ Della porta cipher.  Symmetric.

    Notes
    -----
    This is a variant of the Beaufort cipher, not to be confused with the
    "variant Beaufort" cipher, which is a variant of the Vigenere.

    [TODO] ensure alphabet length is divisible by the number of items in each
    group in the leftmost (key) column

    """
    def _make_alphabets(self, alphabet):
        alpha_len = len(alphabet) // 2  # need an int
        first_half_alphabet = alphabet[:alpha_len]
        second_half_alphabet = alphabet[alpha_len:]

        transcoders = {}
        for i, c in enumerate(alphabet):
            offset = i // 2
            secondhalf = second_half_alphabet.lrotate(offset)
            firsthalf = first_half_alphabet.lrotate(-offset)
            alphabet_ = secondhalf + firsthalf
            transcoders[c] = Transcoder(alphabet, alphabet_)

        return transcoders

    def _cipher(self, msg_char, key_char, reverse=False):
        """ Convert characters from one alphabet to another
        (reverse is ignored) """
        # return super()._cipher(msg_char, key_char, reverse=reverse)
        return self.tabula_recta.decode(msg_char, key_char)
