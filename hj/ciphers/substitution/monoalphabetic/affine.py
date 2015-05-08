# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import Alphabet
from fractions import gcd


class AffineCipher(MonoSubCipher):
    def __init__(self, m, b, alphabet=None):
        """ Shift characters based on mx + b.

        Parameters
        ----------
        m : int
            A multiplier.
        b : int
            An offset.
        alphabet : sequence, optional
            An alphabet.

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

        alphabet = Alphabet(alphabet)
        transformed = alphabet.affinal(m, b)
        super().__init__(alphabet, transformed)
