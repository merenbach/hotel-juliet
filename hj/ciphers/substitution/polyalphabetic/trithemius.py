#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import Alphabet, TabulaRecta


class TrithemiusCipher(VigenereCipher):
    """ Conceptual precursor to Vigenere.

    Notes
    -----
    Not especially secure as passphrase is simply the alphabet.

    """
    def __init__(self, alphabet=None):
        alphabet = Alphabet(alphabet)
        super().__init__(alphabet, alphabet=alphabet, autoclave=False)
