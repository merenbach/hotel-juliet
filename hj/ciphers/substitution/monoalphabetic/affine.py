#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.base import coprime


class AffineCipher(MonoSubCipher):
    def __init__(self, m, b, alphabet=None):
        """ Shift characters based on mx + b.

        Parameters
        ----------
        m : int
            A multiplier.
        b : int
            An offset.  Must range from `0` to `len(alphabet) - 1`.
        alphabet : string-like, optional
            An alphabet to use for transcoding.

        """
        self.multiplier, self.offset = m, b
        super().__init__(alphabet)

    def alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

        Raises
        ------
        ValueError
            If multiplier is not coprime with the length of `alphabet`, or
            if offset is greater than or equal to the length of `alphabet`, or
            if offset is less than zero.

        """
        # We're cheating here by not actually having the decryption method
        # use the "inverse" argument
        if not 0 <= self.offset < len(alphabet):
            raise ValueError('Offset out of range [0, <length of alphabet>).')
        if not coprime(self.multiplier, len(alphabet)):
            raise ValueError('Multiplier and alphabet length must be coprime.')
        return alphabet.affinal(self.multiplier, self.offset)
