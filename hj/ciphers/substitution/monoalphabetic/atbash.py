#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher


class AtbashCipher(MonoSubCipher):
    """ Transcode based on reverse alphabet.

    """
    def alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

        """
        return alphabet.reverse()
