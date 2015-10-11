#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import OneWayTranscoder
from collections import OrderedDict


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    a : sequence of str
        A source character set to use for transcoding.
    b : sequence of str
        A target character set to use for transcoding.

    """
    def __init__(self, a, b):
        super().__init__(a)
        self.a2b, self.b2a = OneWayTranscoder(a, b), OneWayTranscoder(b, a)

    def __str__(self):
        return self.a2b.p(delimiter=',\n ', keyvalsep=' <=> ')

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.a2b.p())

    def _encode(self, s):
        """ Transcode forwards.

        Parameters
        ----------
        s : iterable
            An iterable of elements to transcode.

        Returns
        -------
        out : generator
            The transcoded counterparts, if possible, of the input sequence.

        """
        return (self.a2b.get(e, e) for e in s)

    def _decode(self, s):
        """ Transcode backwards.

        Parameters
        ----------
        s : iterable
            An iterable of elements to transcode.

        Returns
        -------
        out : generator
            The transcoded counterparts, if possible, of the input sequence.

        """
        return (self.b2a.get(e, e) for e in s)
