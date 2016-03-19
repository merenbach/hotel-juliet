#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .shift import ShiftCipher
from utils import multiplied


class AffineCipher(ShiftCipher):
    """ Transcode based on a transformation of `mx + b` for multiplier `m`,
    character `x`, and added offset `b`.

    Parameters
    ----------
    multiplier : int,
        A multiplier.  Must be coprime with length of alphabet used.
    offset : int
        An offset.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    The inverse affine operation is complicated mathematically so we "cheat" by
    caching a tableau (as we do for other monoalphabetic ciphers) and using
    that for encoding (forward) and decoding (reverse).

    This may be less secure than some other monoalphabetic ciphers because it
    is vulnerable not only to frequency analysis, but also has an algebraic
    solution that, when computed, reveals the whole ciphertext alphabet.

    """
    def __init__(self, multiplier, offset, alphabet=None):
        self.multiplier = multiplier
        super().__init__(offset, alphabet=alphabet)

    def _transform(self, alphabet):
        alphabet_ = super()._transform(alphabet)
        return multiplied(alphabet_, self.multiplier)
