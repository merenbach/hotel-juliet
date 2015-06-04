#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher
from utils import DEFAULT_ALPHABET


class AtbashCipher(AffineCipher):
    """ Transcode based on reverse alphabet.

    Attributes
    ----------
    DEFAULT_M : int
        The multiplier for the affine cipher.
    DEFAULT_B : int
        The offset for the affine cipher.

    Parameters
    ----------
    alphabet : str, optional
        A character set to use for transcoding.  Default from `utils`.

    Notes
    -----
    The reversal of an alphabet represents a special case of the affine cipher,
    where multiplier and offset are both equal to one less than the length of
    the alphabet.  Thanks to modular arithmetic, values of `-1` for offset and
    multiplier yield the same outcome, without even needing to know the length
    of the alphabet.

    Technically we could simply subclass a generic monoalphabetic substitution
    cipher and invoke `super().__init__(alphabet, reversed(alphabet))`.  That's
    less fun.  [TODO]?

    """
    DEFAULT_M = (-1)
    DEFAULT_B = (-1)

    def __init__(self, alphabet=DEFAULT_ALPHABET):
        super().__init__(self.DEFAULT_M, self.DEFAULT_B, alphabet=alphabet)
