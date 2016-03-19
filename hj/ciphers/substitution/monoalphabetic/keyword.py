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
        A plaintext alphabet.  Default `None`.

    """
    def __init__(self, keyword, alphabet=None):
        self.keyword = keyword
        super().__init__(alphabet)

    def _transform(self, alphabet):
        return keyed(alphabet, self.keyword)
