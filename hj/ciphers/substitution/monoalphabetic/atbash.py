#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher


class AtbashCipher(AffineCipher):
    """ Transcode based on reverse alphabet.

    Parameters
    ----------
    charset : str, optional
        A character set to use for transcoding.  Default `None`.

    Notes
    -----
    This is a special case of the affine cipher where multiplier and offset are
    both equal to `len(alphabet) - 1`.  Since the affine machinery wraps, we
    can pass `-1` to `super()` without even knowing the length of the alphabet.

    """
    def __init__(self, charset=None):
        super().__init__(-1, -1, charset=charset)
