# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import Alphabet


class CaesarShiftCipher(MonoSubCipher):
    """ Shift letters based on a number.

    Parameters
    ----------
    alphabet : utils.alphabet.Alphabet
        An alphabet.
    shift : int
        Shift by this many positions.

    """
    def __init__(self, alphabet=None, shift=3):
        if not alphabet:
            alphabet = Alphabet()
        transformed = alphabet << shift
        super().__init__(alphabet, transformed)
