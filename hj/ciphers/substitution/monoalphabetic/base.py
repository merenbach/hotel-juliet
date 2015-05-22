#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils.alphabet import Alphabet
from utils.transcoder import Transcoder


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    charset : str
        A character set to use for transcoding.
    transform : function
        A function or lambda to transform the alphabet.

    """
    def __init__(self, charset, transform):
        alphabet = Alphabet(charset)
        alphabet_ = transform(alphabet)
        tableau = Transcoder(alphabet, alphabet_)
        super().__init__(tableau)

    def _restrict(self, s):
        """ Clean characters for strict mode.

        """
        return self.tableau.sanitize(s)

    def _encode(self, s):
        return self.tableau.encode(s)

    def _decode(self, s):
        return self.tableau.decode(s)
