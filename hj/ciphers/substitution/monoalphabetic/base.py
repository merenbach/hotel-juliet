#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import OneToOneTranslationTable


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str
        A plaintext alphabet.

    """
    def __init__(self, alphabet):
        super().__init__()

        if not alphabet:
            alphabet = self.DEFAULT_ALPHABET
        alphabet_ = ''.join(self._transform(alphabet))
        self.tableau = OneToOneTranslationTable(alphabet, alphabet_)

    def __repr__(self):
        return '{} ({})'.format(type(self).__name__, repr(self.tableau))

    def __str__(self):
        return str(self.tableau)

    def _transform(self, alphabet):
        """ Create a ciphertext alphabet.

        Returns
        -------
        out : str
            A ciphertext alphabet.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError

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
