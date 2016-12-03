#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import UserList
import string

class Alphabet(UserList):
    """ Wrap an alphabet for use in transcoding.

    Parameters
    ----------
    initlist : sequence of str
        An alphabet for use in transcoding.

    """
    def __init__(self, initlist=None):
        if initlist is None:
            initlist = string.ascii_uppercase
        super().__init__(initlist=initlist)

    def __str__(self):
        return ''.join(self.data)

    def xtable(self, other):
        """ Create a translation table mapping this alphabet to another.

        Parameters
        ----------
        other : sequence
            An alphabet to which to map.  If it is not the same leng

        Returns
        -------
        out : dict
            A map of this alphabet to `other`.

        Raises
        ------
        ValueError
            If this alphabet and `other` have different lengths.

        """
        if len(self.data) != len(other):
            raise ValueError('alphabet length mismatch')
        return dict(zip(self.data, other))
