#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import TransCipher
from utils import grouper, roundrobin

NULLCHAR = 'X'


class ScytaleCipher(TransCipher):
    """ Transcode based on a numeric shift.

    Parameters
    ----------
    key : int
        The number of characters per row.
    alphabet : str, optional
        A character set to use for transcoding.  Default `None`.

    Notes
    -----
    This is far less polished than the other ciphers.  Given time...

    """
    def _encode(self, s):
        groups = grouper(s, self.key, fillvalue=NULLCHAR)
        return roundrobin(*groups)

    def _decode(self, s):
        groups = grouper(s, len(s) // self.key, fillvalue=NULLCHAR)
        return roundrobin(*groups)
