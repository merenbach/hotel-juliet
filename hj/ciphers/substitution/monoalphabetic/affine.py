#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import OneToOneTranslationTable, lcg


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
    ValueError
        If `multiplier` is not coprime with the length of the alphabet.

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
        self.key = (multiplier, shift)
        super().__init__(alphabet=alphabet)

    def maketableau(self, alphabet):
        gen = lcg(len(alphabet), 1, self.key[0], self.key[1])
        alphabet_ = ''.join(alphabet[ next(gen) ] for __ in alphabet)
        return OneToOneTranslationTable(alphabet, alphabet_)
