#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher


class DecimationCipher(AffineCipher):
    """ Transcode based on a transformation of `mx` for multiplier `m` and
    character `x`.

    Attributes
    ----------
    DEFAULT_SHIFT : int
        The defined shift (0 places) for a decimation cipher.
        Exists as a named variable to avoid a "magic number."

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
    DEFAULT_SHIFT = 0

    def __init__(self, multiplier, alphabet=None):
        super().__init__(multiplier, self.DEFAULT_SHIFT, alphabet=alphabet)
