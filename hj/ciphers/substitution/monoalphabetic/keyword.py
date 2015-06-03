#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import DEFAULT_ALPHABET, keyed


class KeywordCipher(MonoSubCipher):
    """ Transcode based on a keyword.

    Parameters
    ----------
    keyword : str
        A keyword for transcoding.
    alphabet : str, optional
        A character set to use for transcoding.  Default from `utils`.

    """
    def __init__(self, keyword, alphabet=DEFAULT_ALPHABET):
        alphabet_ = keyed(alphabet, keyword)
        super().__init__(alphabet, alphabet_)
