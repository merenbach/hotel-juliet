#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import OneToOneTranslationTable


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    """
    def maketableau(self, alphabet):
        alphabet, alphabet_ = self.makealphabets(alphabet, key=self.key)
        return OneToOneTranslationTable(alphabet, alphabet_)

    def _encode(self, s):
        """ Encode a message.

        Parameters
        ----------
        s : str
            A message to transcode.

        Yields
        ------
        out : str
            A transcoded version of `s`.

        """
        for c in s:
            yield self.tableau.encipher(c)

    def _decode(self, s):
        """ Decode a message.

        Parameters
        ----------
        s : str
            A message to transcode.

        Yields
        ------
        out : str
            A transcoded version of `s`.

        """
        for c in s:
            yield self.tableau.decipher(c)
