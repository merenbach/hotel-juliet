#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import MonoSubCipher
from utils import OneToOneTranslationTable, unique


class KeywordCipher(MonoSubCipher):
    """ Transcode based on a keyword.

    Parameters
    ----------
    keyword : str
        A keyword for transcoding.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    If the keyword contains at least one occurrence every character in the
    alphabet in use, those characters (with repetitions, consecutive or not,
    ignored) become the full ciphertext alphabet.

    This will provide the same output as any other monoalphabetic substitution
    cipher if the relevant ciphertext alphabet is provided as the keyword.

    """
    def __init__(self, keyword, alphabet=None):
        self.key = keyword
        super().__init__(alphabet=alphabet)

    def maketableau(self, alphabet):
        alphabet_ = ''.join(unique(alphabet, prefix=self.key))
        return OneToOneTranslationTable(alphabet, alphabet_)
