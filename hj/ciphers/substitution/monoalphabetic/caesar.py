#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher


class CaesarCipher(AffineCipher):
    """ Transcode based on a numeric shift (three positions, by default).

    Attributes
    ----------
    DEFAULT_M: int
        A multiplier of one, since we're simply shifting.
        Exists as a named variable to avoid a "magic number."
    DEFAULT_B : int
        The traditional shift (3 places) for a Caesar cipher.
        Exists as a named variable to avoid a "magic number."

    Parameters
    ----------
    offset : int, optional
        An integer offset for transcoding.  Default `3`.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    This is a special case of the affine cipher with a multiplier of one.

    """
    DEFAULT_M = 1
    DEFAULT_B = 3

    def __init__(self, offset=DEFAULT_B, alphabet=None):
        super().__init__(self.DEFAULT_M, offset, alphabet=alphabet)
