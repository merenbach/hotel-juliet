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
    alphabet : str, optional
        A character set to use for transcoding.  Default `None`.

    """
    def __init__(self, keyword, alphabet=None):
        transform = lambda a: keyed(a, keyword)
        super().__init__(transform, alphabet=alphabet)
