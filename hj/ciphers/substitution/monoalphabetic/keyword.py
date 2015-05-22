#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import keyed


class KeywordCipher(MonoSubCipher):
    """ Transcode based on a keyword.

    Parameters
    ----------
    keyword : str
        A keyword for transcoding.
    charset : str, optional
        An alphabet to use for transcoding.  Default `None`.

    """
    def __init__(self, keyword, charset=None):
        transform = lambda c: keyed(c, keyword)
        super().__init__(charset, transform)
