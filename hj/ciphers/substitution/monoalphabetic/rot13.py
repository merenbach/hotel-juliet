#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .caesar import CaesarCipher


class Rot13Cipher(CaesarCipher):
    """ Transcode the ASCII alphabet based on 13-character rotation.

    Attributes
    ----------
    DEFAULT_SHIFT : int
        The defined shift (13 places) for a ROT13 cipher.
        Exists as a named variable to avoid a "magic number."

    Notes
    -----
    This is a special case of the Caesar cipher with a shift of `13`.

    """
    DEFAULT_SHIFT = 13

    def __init__(self):
        super().__init__(self.DEFAULT_SHIFT)
