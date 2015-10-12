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
    verbose_name = 'keyword'

    def __init__(self, keyword, alphabet=None):
        super().__init__(alphabet)
        self.keyword = keyword

    def alphabet_(self):
        alphabet_ = keyed(self.alphabet, self.keyword)
        return ''.join(alphabet_)
