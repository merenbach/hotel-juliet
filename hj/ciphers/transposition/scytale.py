#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import TransCipher
from utils import grouper, roundrobin

NULLCHAR = 'X'


class ScytaleCipher(TransCipher):
    """ Transcode based on a numeric shift.

    Parameters
    ----------
    length : int
        The number of characters per row.
    charset : str, optional
        A character set to use for transcoding.  Default `None`.

    """
    def __init__(self, length, charset=None):
        self.length = length
        # self.depth =
        super().__init__()

    def _encode(self, s):
        groups = grouper(s, self.length, fillvalue=NULLCHAR)
        return roundrobin(*groups)

    def _decode(self, s):
        groups = grouper(s, len(s) // self.length, fillvalue=NULLCHAR)
        return roundrobin(*groups)

    def encode(self, s, strict):
        # [TODO] this assumes left-to-right message text direction...
        transcoded = self._encode(s)
        return ''.join(transcoded)

    def decode(self, s, strict):
        # [TODO] this assumes left-to-right message text direction...
        transcoded = self._decode(s)
        return ''.join(transcoded).rstrip(NULLCHAR)
