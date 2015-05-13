#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.base import coprime
from .caesar_shift import CaesarShiftCipher


class AffineCipher(CaesarShiftCipher):
    """ Transcode based on mx + b.

    Attributes
    ----------
    DEFAULT_MULTIPLIER : int
        With the default value of 1, this becomes a Caesar cipher.
    # DEFAULT_SHIFT : int
    #     The traditional shift (3 places) for a Caesar cipher.
    #     Exists as a named variable to avoid a "magic number."


    Parameters
    ----------
    offset : int
        An offset.  Must range from `0` to `len(alphabet) - 1`.
    multiplier : int
        A multiplier.
    alphabet : string-like, optional
        An alphabet to use for transcoding.

    """
    DEFAULT_MULTIPLIER = 1

    def __init__(self, multiplier=None, offset=None, alphabet=None):
        if not multiplier:
            multiplier = self.DEFAULT_MULTIPLIER
        self.multiplier = multiplier
        super().__init__(offset=offset, alphabet=alphabet)

    def alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

        Raises
        ------
        ValueError
            If multiplier is not coprime with the length of `alphabet`, or
            if offset is greater than or equal to the length of `alphabet`, or
            if offset is less than zero.

        Notes
        -----
        We're "cheating" here by not actually having the decryption machinery
        run any inverse operations and by invoking `super()` to create an
        offset alphabet that we then "multiply."  Without this cleverness,
        our multiplication would be:

            (self.multiplier * n + self.offset) mod len(alphabet)

        """
        if not 0 <= self.offset < len(alphabet):
            raise ValueError('Offset out of range [0, <length of alphabet>).')

        # first run Caesar cipher shifts
        alphabet = super().alphabet_(alphabet)

        # now let's multiply some letters
        return alphabet.multiply(self.multiplier)
