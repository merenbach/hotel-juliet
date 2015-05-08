#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import Alphabet


def coprime(a, b):
    """ Determine whether `a` and `b` are coprime.

    """
    from fractions import gcd
    return gcd(a, b) == 1


class AffineCipher(MonoSubCipher):
    def __init__(self, m, b, alphabet=None):
        """ Shift characters based on mx + b.

        Parameters
        ----------
        m : int
            A multiplier.
        b : int
            An offset.  Must range from `0` to `len(alphabet) - 1`.
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
        if not 0 <= b < len(alphabet):
            raise ValueError('Offset out of range [0, <length of alphabet>).')
        if not coprime(m, len(alphabet)):
            raise ValueError('Multiplier and alphabet length must be coprime.')

        alphabet = Alphabet(alphabet)
        transformed = alphabet.affinal(m, b)
        super().__init__(alphabet, transformed)
