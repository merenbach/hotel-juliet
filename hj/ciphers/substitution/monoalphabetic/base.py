#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import OneToOneTranslationTable


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    key : str
        An encryption/decryption key.   May be an integer, tuple, etc.
        It will be passed to the `_transform` method.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    """
    def __init__(self, key, alphabet=None):
        super().__init__()

        if not alphabet:
            alphabet = self.DEFAULT_ALPHABET
        alphabet_ = ''.join(self._transform(alphabet, key))
        self.tableau = OneToOneTranslationTable(alphabet, alphabet_)

    def __repr__(self):
        return '{} ({})'.format(type(self).__name__, repr(self.tableau))

    def __str__(self):
        return str(self.tableau)

    @staticmethod
    def _transform(alphabet, key):
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
