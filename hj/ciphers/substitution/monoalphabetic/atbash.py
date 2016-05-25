#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .affine import AffineCipher


class AtbashCipher(AffineCipher):
    """ Transcode based on reverse alphabet.

    Parameters
    ----------
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    This is a special case of the affine cipher with a multiplier and shift
    both equal to one less than the length of the alphabet in use.  Thanks to
    Python modular arithmetic, we can specify `-1` for both of these to achieve
    the same result without knowing the length of the alphabet beforehand.

    Technically we could simply subclass the generic MonoSubCipher class and
    invoke `super().__init__(alphabet, alphabet[::-1])`.

    """
    def __init__(self, alphabet=None):
        super().__init__(-1, -1, alphabet=alphabet)
