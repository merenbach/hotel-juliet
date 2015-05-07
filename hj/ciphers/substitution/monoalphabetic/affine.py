# -*- coding: utf-8 -*-

from . import MonoSubCipher
from fractions import gcd


class AffineCipher(MonoSubCipher):
    def __init__(self, alphabet, m, b):
        """ Shift letters based on mx + b.

        Parameters
        ----------
        alphabet : utils.alphabet.alphabet
            An alphabet.
        m : int
            A multiplier.
        b : int
            An offset.

        Raises
        ------
        ValueError
            If multiplier is not coprime with the length of `alphabet`, or
            if offset is greater than or equal to the length of `alphabet`, or
            if offset is less than zero.

        """
        # We're cheating here by not actually having the decryption method
        # use the "inverse" argument
        if b < 0:
            raise ValueError('Offset cannot be less than zero.')
        if b >= len(alphabet):
            raise ValueError('Offset must be less than length of alphabet.')
        if gcd(m, len(alphabet)) != 1:
            raise ValueError('Multiplier and alphabet length must be coprime.')

        transformed = alphabet.affinal(m, b)
        super().__init__(alphabet, transformed)
