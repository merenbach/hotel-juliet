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
    The reversal of an alphabet represents a special case of the affine cipher,
    where multiplier and offset are both equal to one less than the length of
    the alphabet.  Thanks to modular arithmetic, values of `-1` for offset and
    multiplier yield the same outcome, without even needing to know the length
    of the alphabet.

    """
    def __init__(self, charset=None):
        super().__init__(-1, -1, charset=charset)
