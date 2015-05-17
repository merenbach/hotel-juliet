#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .caesar import CaesarCipher


class AffineCipher(CaesarCipher):
    """ Transcode based on mx + b.

    Attributes
    ----------
    DEFAULT_M : int
        With the default value of 1, this becomes a Caesar cipher.
    DEFAULT_B : int
        A default shift of 0.
        Exists as a named variable to avoid a "magic number."

    Parameters
    ----------
    multiplier : int, optional
        A multiplier.
    offset : int, optional
        An offset.  Must range from `0` to `len(alphabet) - 1`.
    alphabet : string-like, optional
        An alphabet to use for transcoding.

    Notes
    -----
    Although this cipher is technically different from a Caesar shift,
    the alphabet offset functions the same way so we simply extend the
    Caesar cipher implementation to add a multiplier.

    """
    DEFAULT_M = 1
    DEFAULT_B = 0

    def __init__(self, multiplier=DEFAULT_M, offset=DEFAULT_B, alphabet=None):
        self.multiplier = multiplier
        super().__init__(offset=offset, alphabet=alphabet)

    def make_alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

        # Raises
        # ------
        # ValueError
        #     If multiplier is not coprime with the length of `alphabet`, or
        #     if offset is greater than or equal to the length of `alphabet`,
        #     or if offset is less than zero.

        Notes
        -----
        We're "cheating" here by not actually having the decryption machinery
        run any inverse operations and by invoking `super()` to create an
        offset alphabet that we then "multiply."  Without this second bit of
        cleverness, our multiplication would be:

            (self.multiplier * n + self.offset) mod len(alphabet)

        [TODO] Make this mechanism more elegant

        """
        # first run Caesar cipher shifts
        alphabet = super().make_alphabet_(alphabet)

        # now let's multiply some letters
        return alphabet.multiply(self.multiplier)
