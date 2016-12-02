#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import UserList
import string

class Alphabet(UserList):
    """ Wrap an alphabet for use in transcoding.

    Parameters
    ----------
    initstr : str
        An alphabet for use in transcoding.

    """
    def __init__(self, initstr=None):
        if initstr is None:
            initstr = string.ascii_uppercase
        super().__init__(initlist=initstr)

    def __str__(self):
        return ''.join(self.data)
