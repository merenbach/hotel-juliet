#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import lrotated


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
        An integer offset for transcoding.  Default `DEFAULT_OFFSET`.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    """
    verbose_name = 'Caesar'

    DEFAULT_OFFSET = 3

    def __init__(self, offset=DEFAULT_OFFSET, alphabet=None):
        super().__init__(alphabet)
        self.offset = offset

    def alphabet_(self):
        alphabet_ = lrotated(self.alphabet, self.offset)
        return ''.join(alphabet_)
