#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher


class AtbashCipher(AffineCipher):
    """ Transcode based on reverse alphabet.

    Notes
    -----
    This is a special case of the affine cipher where both the multiplier and
    offset are equal to `len(alphabet) - 1`.  Since our alphabets wrap, we can
    pass `-1` to `super()` without even knowing the length of the alphabet.

    """
    def __init__(self, alphabet=None):
        super().__init__(-1, -1, alphabet=alphabet)
