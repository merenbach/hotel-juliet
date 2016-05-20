#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher
from utils import mod_sequence


class DecimationCipher(AffineCipher):
    """ Transcode based on a transformation of `mx` for multiplier `m` and
    character `x`.

    Attributes
    ----------
    DEFAULT_B : int
        A shift of zero places, since we're simply multiplying.
        Exists as a named variable to avoid a "magic number."

    Parameters
    ----------
    key : int
        A multiplier.  Must be coprime with length of alphabet used.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    This is a special case of the affine cipher with an offset/shift of zero.

    """
    DEFAULT_B = 0

    def __init__(self, key, alphabet=None):
        super().__init__(key, self.DEFAULT_B, alphabet=alphabet)
