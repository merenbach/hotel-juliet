#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import Alphabet


class KeywordCipher(MonoSubCipher):
    """ Shift characters based on a keyword.

    Parameters
    ----------
    keyword : str
        A keyword.
    alphabet : sequence, optional
        An alphabet.

    """
    def __init__(self, keyword, alphabet=None):
        alphabet = Alphabet(alphabet)
        transformed = alphabet.keyed(keyword)
        super().__init__(alphabet, transformed)
