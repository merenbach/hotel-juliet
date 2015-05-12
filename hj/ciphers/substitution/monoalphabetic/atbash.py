#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import MonoSubCipher
from utils.alphabet import AlphabetReverseOperation


class AtbashCipher(MonoSubCipher):
    """ Shift letters based on reverse alphabet.

    Parameters
    ----------
    alphabet : string-like, optional
        An alphabet to use for transcoding.

    """
    def __init__(self, alphabet=None):
        operations = [AlphabetReverseOperation()]
        super().__init__(alphabet, operations)
