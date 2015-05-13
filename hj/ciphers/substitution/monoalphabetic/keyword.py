#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher


class KeywordCipher(MonoSubCipher):
    """ Transcode based on a keyword.

    Parameters
    ----------
    keyword : str
        A keyword for transcoding.
    alphabet : string-like, optional
        An alphabet to use for transcoding.

    """
    def __init__(self, keyword, alphabet=None):
        self.keyword = keyword
        super().__init__(alphabet)

    def alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

        """
        return alphabet.keyed(self.keyword)
