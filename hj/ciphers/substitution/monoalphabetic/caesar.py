#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import DEFAULT_ALPHABET, lrotated


class CaesarCipher(MonoSubCipher):
    """ Transcode based on a numeric shift.

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
        A character set to use for transcoding.  Default `None`.

    """
    DEFAULT_OFFSET = 3

    def __init__(self, offset=DEFAULT_OFFSET, alphabet=DEFAULT_ALPHABET):
        alphabet_ = lrotated(alphabet, offset)
        super().__init__(alphabet, alphabet_)
