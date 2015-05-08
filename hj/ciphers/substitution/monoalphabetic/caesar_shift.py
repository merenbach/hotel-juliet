# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import Alphabet


class CaesarShiftCipher(MonoSubCipher):
    """ Shift characters based on a number.

    Parameters
    ----------
    shift : int
        Shift by this many positions.
    alphabet : sequence, optional
        An alphabet.

    Attributes
    ----------
    DEFAULT_SHIFT : int
        The traditional shift (3 places) for a Caesar cipher.
        Here as a variable to avoid a "magic number."

    """
    DEFAULT_SHIFT = 3

    def __init__(self, shift=DEFAULT_SHIFT, alphabet=None):
        alphabet = Alphabet(alphabet)
        transformed = alphabet.rotated(shift)
        super().__init__(alphabet, transformed)
