#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import MonoalphabeticTableau


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str
        A source character set to use for transcoding.
    alphabet_ : str
        A destination character set to use for transcoding.

    """
    def __init__(self, alphabet, alphabet_):
        super().__init__(alphabet)
        self.tableau = MonoalphabeticTableau(alphabet, alphabet_)

    def _encode(self, s, strict):
        return self.tableau.encode(s, not strict)

    def _decode(self, s, strict):
        return self.tableau.decode(s, not strict)
