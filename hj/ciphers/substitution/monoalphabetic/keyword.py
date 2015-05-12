#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import KeyOp


class KeywordCipher(MonoSubCipher):
    """ Shift characters based on a keyword.

    Parameters
    ----------
    keyword : str
        A keyword for transcoding.
    alphabet : string-like, optional
        An alphabet to use for transcoding.

    """
    def __init__(self, keyword, alphabet=None):
        operations = [KeyOp(keyword)]
        super().__init__(alphabet, operations)
