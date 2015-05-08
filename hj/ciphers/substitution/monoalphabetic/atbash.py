# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import Alphabet


class AtbashCipher(MonoSubCipher):
    def __init__(self, alphabet=None):
        """ Shift letters based on reverse alphabet.

        Parameters
        ----------
        alphabet : utils.alphabet.Alphabet, optional
            An alphabet.

        """
        alphabet = Alphabet(alphabet)
        transformed = alphabet.reversed()
        super().__init__(alphabet, transformed)
