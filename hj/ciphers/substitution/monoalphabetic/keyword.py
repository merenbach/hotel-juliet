# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import Alphabet


class KeywordCipher(MonoSubCipher):
    """ Shift letters based on a keyword.

    Parameters
    ----------
    alphabet : utils.alphabet.Alphabet
        An alphabet.
    keyword : str
        A keyword.

    """
    def __init__(self, alphabet=None, keyword=None):
        if not alphabet:
            alphabet = Alphabet()
        transformed = alphabet.keyed(keyword)
        super().__init__(alphabet, transformed)
