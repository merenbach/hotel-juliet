#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher


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
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    The reversal of an alphabet represents a special case of the affine cipher,
    where multiplier and offset are both equal to one less than the length of
    the alphabet.  Thanks to modular arithmetic, values of `-1` for offset and
    multiplier yield the same outcome, without even needing to know the length
    of the alphabet.  Since other language implementations may handle negative
    modular arithmetic differently, for the record, the default M and B could
    also be the alphabet/character set length minus one (e.g., `26` for the
    Latin alphabet).

    Technically we could simply subclass the generic MonoSubCipher class and
    invoke `super().__init__(alphabet, alphabet[::-1])`.

    """
    DEFAULT_M = (-1)
    DEFAULT_B = (-1)

    def __init__(self, alphabet=None):
        super().__init__(self.DEFAULT_M, self.DEFAULT_B, alphabet=alphabet)
