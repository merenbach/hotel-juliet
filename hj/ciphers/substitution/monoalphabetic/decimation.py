#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher


class DecimationCipher(AffineCipher):
    """ Transcode based on a transformation of `mx` for multiplier `m` and
    character `x`.

    Parameters
    ----------
    multiplier : int
        A multiplier.  Must be coprime with length of alphabet used.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Raises
    ------
    ValueError
        If `multiplier` is not coprime with the length of the alphabet.

    Notes
    -----
    This is a special case of the affine cipher with a shift of `0`.

    """
    def __init__(self, multiplier, alphabet=None):
        super().__init__(multiplier, 0, alphabet=alphabet)
