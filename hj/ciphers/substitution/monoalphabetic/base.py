#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    """
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
