#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher


class AtbashCipher(MonoSubCipher):
    """ Shift letters based on reverse alphabet.

    """
    def alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

        Parameters
        ----------
        alphabet : utils.alphabet.Alphabet
            An alphabet to transform.

        """
        return ~alphabet
