#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import OneWayTranscoder


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
        super().__init__()
        self.a2b, self.b2a = OneWayTranscoder(a, b), OneWayTranscoder(b, a)

    def __str__(self):
        return self.a2b.p(delimiter=',\n ', keyvalsep=' <=> ')

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.a2b.p())

    def _encode(self, s, strict):
        """ Transcode forwards.

        Parameters
        ----------
        s : iterable
            An iterable of elements to transcode.
        strict : bool
            `True` to skip non-transcodable elements,
            `False` to yield them unchanged.

        Returns
        -------
        out : data-type
            The transcoded counterparts, if possible, of the input sequence.

        """
        return self.a2b.transcode(s, strict)

    def _decode(self, s, strict):
        """ Transcode backwards.

        Parameters
        ----------
        s : iterable
            An iterable of elements to transcode.
        strict : bool
            `True` to skip non-transcodable elements,
            `False` to yield them unchanged.

        Returns
        -------
        out : data-type
            The transcoded counterparts, if possible, of the input sequence.

        """
        return self.b2a.transcode(s, strict)
