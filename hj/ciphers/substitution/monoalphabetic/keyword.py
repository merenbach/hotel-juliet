#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher


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
        self.keyword = keyword
        super().__init__(charset)

    def _make_alphabet(self, alphabet):
        """ Create a transcoding alphabet.

        """
        return alphabet.keyed(self.keyword)
