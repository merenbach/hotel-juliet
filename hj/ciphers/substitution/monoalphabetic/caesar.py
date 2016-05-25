#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher


class CaesarCipher(AffineCipher):
    """ Transcode based on a numeric shift (three positions, by default).

    Attributes
    ----------
    DEFAULT_SHIFT : int
        The traditional shift (3 places) for a Caesar cipher.
        Exists as a named variable to avoid a "magic number."

    Parameters
    ----------
    shift : int, optional
        An integer offset for transcoding.  Default `3`.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    This is a special case of the affine cipher with a multiplier of `1`.

    """
    DEFAULT_SHIFT = 3

    def __init__(self, shift=DEFAULT_SHIFT, alphabet=None):
        super().__init__(1, shift, alphabet=alphabet)
