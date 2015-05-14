#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher


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
        An integer offset for transcoding.
    alphabet : string-like, optional
        An alphabet to use for transcoding.

    """
    DEFAULT_OFFSET = 3

    def __init__(self, offset=DEFAULT_OFFSET, alphabet=None):
        self.offset = offset
        super().__init__(alphabet)

    def make_alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

        """
        return alphabet.lrotate(self.offset)
