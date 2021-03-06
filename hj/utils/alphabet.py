#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import UserList
from utils import lrotated
import string


class BaseAlphabet(UserList):
    """ Wrap an alphabet for use in transcoding.

    Parameters
    ----------
    initlist : sequence, optional
        An alphabet for use in transcoding.  Default `None`.
        (If omitted, will be replaced with an empty list.)

    Raises
    ------
    ValueError
        If any elements in `initlist` recur.

    Notes
    -----
    [TODO] unit tests required

    """
    def __init__(self, initlist=None):
        if self.recurrences(initlist or []) > 0:
            raise ValueError('values in alphabet may not recur')
        super().__init__(initlist=initlist)

    @staticmethod
    def recurrences(seq):
        """ Find the count of repeated elements.

        Parameters
        ----------
        seq : sequence
            A sequence to evaluate.

        Returns
        -------
        out : int
            The number of recurrences, or `0` if none.

        Notes
        -----
        If a single element recurs multiple times, each additional recurrence
        will count.

        """
        return len(seq) - len(set(seq))


class Alphabet(BaseAlphabet):
    """ Wrap an alphabet for use in transcoding.

    Attributes
    ----------
    DEFAULT_ALPHABET : str
        The default character set for encoding.
    DEFAULT_NULLCHAR : str
        A default string ("X") to use as padding.

    Parameters
    ----------
    initlist : sequence of str, optional
        An alphabet for use in transcoding.  Default `None`.
        (If omitted, will be replaced with `string.ascii_uppercase`.)

    """
    DEFAULT_ALPHABET = string.ascii_uppercase
    DEFAULT_NULLCHAR = 'X'

    def __init__(self, initlist=None):
        if initlist is None:
            initlist = self.DEFAULT_ALPHABET
        super().__init__(initlist=initlist)

    def __str__(self):
        return ''.join(self)
