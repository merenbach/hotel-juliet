#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher


class CaesarShiftCipher(MonoSubCipher):
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

    def __init__(self, offset=None, alphabet=None):
        if offset is None:
            offset = self.DEFAULT_OFFSET
        self.offset = offset
        super().__init__(alphabet)

    def alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

        """
        return alphabet << self.offset
