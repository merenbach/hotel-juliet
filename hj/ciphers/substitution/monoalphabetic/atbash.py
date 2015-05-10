#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import Alphabet


class AtbashCipher(MonoSubCipher):
    def __init__(self, alphabet=None):
        """ Shift letters based on reverse alphabet.

        Parameters
        ----------
        alphabet : sequence, optional
            An alphabet.

        """
        alphabet = Alphabet(alphabet)
        transformed = ~alphabet
        super().__init__(alphabet, transformed)
