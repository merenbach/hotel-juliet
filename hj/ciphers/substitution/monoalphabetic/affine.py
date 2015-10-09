#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import DEFAULT_ALPHABET, affine_transform


class AffineCipher(MonoSubCipher):
    """ Transcode based on a transformation of `mx + b` for multiplier `m`,
    character `x`, and added offset `b`.

    Parameters
    ----------
    multiplier : int,
        A multiplier.  Must be coprime with length of alphabet used.
    offset : int
        An offset.
    alphabet : str, optional
        A character set to use for transcoding.  Default from `utils`.

    Notes
    -----
    Although this cipher is technically different from a Caesar shift, the
    behavioral outcome here is, interestingly enough, the same as if we'd run a
    Caesar shift and then multiplied the letters with an added offset of zero.

    The inverse affine operation is complicated mathematically so we "cheat" by
    caching a tableau (as we do for other monoalphabetic ciphers) and using
    that for encoding (forward) and decoding (reverse).

    This may be less secure than some other monoalphabetic ciphers because it
    is vulnerable not only to frequency analysis, but also has an algebraic
    solution that, when computed, reveals the whole ciphertext alphabet.

    """
    def __init__(self, multiplier, offset, alphabet=DEFAULT_ALPHABET):
        alphabet_ = affine_transform(alphabet, multiplier, offset)
        super().__init__(alphabet, alphabet_)
