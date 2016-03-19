#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .shift import ShiftCipher


class CaesarCipher(ShiftCipher):
    """ Transcode based on a numeric shift of 3.

    Attributes
    ----------
    DEFAULT_OFFSET : int
        The traditional shift (3 places) for a Caesar cipher.
        Exists as a named variable to avoid a "magic number."

    Parameters
    ----------
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    """
    DEFAULT_OFFSET = 3

    def __init__(self, alphabet=None):
        super().__init__(self.DEFAULT_OFFSET, alphabet=alphabet)
