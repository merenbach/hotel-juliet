#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .caesar import CaesarCipher


class AffineCipher(CaesarCipher):
    """ Transcode based on mx + b.

    Parameters
    ----------
    multiplier : int,
        A multiplier.  Must be coprime with length of alphabet used.
    offset : int
        An offset.
    alphabet : string-like, optional
        An alphabet to use for transcoding.

    Notes
    -----
    Although this cipher is technically different from a Caesar shift,
    the alphabet offset functions the same way so we simply extend the
    Caesar cipher implementation to add a multiplier.

    """
    def __init__(self, multiplier, offset, alphabet=None):
        self.multiplier = multiplier
        super().__init__(offset=offset, alphabet=alphabet)

    def make_alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

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
