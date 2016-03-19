#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import lrotated


class ShiftCipher(MonoSubCipher):
    """ Transcode based on a numeric shift.

    Parameters
    ----------
    offset : int
        An integer offset for transcoding.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    """
    def __init__(self, offset, alphabet=None):
        self.offset = offset
        super().__init__(alphabet)

    def _transform(self, alphabet):
        return lrotated(alphabet, self.offset)
