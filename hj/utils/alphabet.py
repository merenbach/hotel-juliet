#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import UserString
import string

class Alphabet(UserString):
    """ Wrap an alphabet, which is most likely to be a string.

    Parameters
    ----------
    seq : sequence
        An alphabet for use in transcoding.

    """
    def __init__(self, seq=None):
        if seq is None:
            seq = string.ascii_uppercase
        super().__init__(seq)
