#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import AlphabetShiftOperation


class CaesarShiftCipher(MonoSubCipher):
    """ Shift based on a number.

    Attributes
    ----------
    DEFAULT_SHIFT : int
        The traditional shift (3 places) for a Caesar cipher.
        Exists as a named variable to avoid a "magic number."

    Parameters
    ----------
    shift : int
        An integer offset for transcoding.
    alphabet : string-like, optional
        An alphabet to use for transcoding.

    """
    DEFAULT_SHIFT = 3

    def __init__(self, shift=DEFAULT_SHIFT, alphabet=None):
        operations = [AlphabetShiftOperation(shift)]
        super().__init__(alphabet, operations)
