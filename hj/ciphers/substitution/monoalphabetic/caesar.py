#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import lrotated


class CaesarCipher(MonoSubCipher):
    """ Transcode based on a numeric shift (three positions, by default).

    Attributes
    ----------
    DEFAULT_OFFSET : int
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
    Technically, the affine cipher is just a Caesar shift cipher with the
    additional step of transforming the alphabet further after shifting it.

    Technically, a Caesar shift cipher is just an affine cipher with a
    multiplier of `1`.

    """
    DEFAULT_OFFSET = 3

    def __init__(self, offset=DEFAULT_OFFSET, alphabet=None):
        self.offset = offset
        super().__init__(alphabet=alphabet)

    def _transform(self, alphabet):
        return lrotated(alphabet, self.offset)
