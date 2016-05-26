#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    """
    def __init__(self, alphabet=None):
        super().__init__(alphabet)

    def __repr__(self):
        return '{} ({})'.format(type(self).__name__, repr(self.tableau))

    def __str__(self):
        return str(self.tableau)

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
