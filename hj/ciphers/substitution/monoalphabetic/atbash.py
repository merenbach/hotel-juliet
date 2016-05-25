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
    both equal to one less than the length of the alphabet in use, which
    effectively reverses the string..  Thanks to Python modular arithmetic,
    we can specify `-1` for both of these to achieve the same result without
    knowing the length of the alphabet beforehand.

    """
    def __init__(self, alphabet=None):
        super().__init__(-1, -1, alphabet=alphabet)
