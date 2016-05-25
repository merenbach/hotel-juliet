#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import lcg
import itertools


class AffineCipher(MonoSubCipher):
    """ Transcode based on a transformation of `mx + b` for multiplier `m`,
    character `x`, and added offset `b`.

    Parameters
    ----------
    multiplier : int
        A multiplier.  Must be coprime with length of alphabet used.
    shift : int
        An offset.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Raises
    ------

    Notes
    -----
    The inverse affine operation is complicated mathematically so we "cheat" by
    caching a tableau (as we do for other monoalphabetic ciphers) and using
    that for encoding (forward) and decoding (reverse).

    This may be less secure than some other monoalphabetic ciphers because it
    is vulnerable not only to frequency analysis, but also has an algebraic
    solution that, when computed, reveals the whole ciphertext alphabet.

    Technically, the affine cipher can be implemented as a Caesar shift
    cipher with the additional step of transforming the alphabet
    further after shifting it.

    """
    def __init__(self, multiplier, shift, alphabet=None):
        key = (multiplier, shift)
        super().__init__(key, alphabet=alphabet)

    @staticmethod
    def _transform(alphabet, key):
        count = len(alphabet)
        generator = itertools.islice(lcg(count, 1, key[0], key[1]), count)
        return ''.join(alphabet[n] for n in generator)
