# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import Alphabet


class AtbashCipher(MonoSubCipher):
    def __init__(self, alphabet=None, processor=None):
        """ Reverse alphabet.

        Parameters
        ----------
        alphabet : utils.alphabet.Alphabet
            An alphabet.
        processor : ...

        """
        if not alphabet:
            alphabet = Alphabet()
        transformed = alphabet.reversed()
        super().__init__(alphabet, transformed)
