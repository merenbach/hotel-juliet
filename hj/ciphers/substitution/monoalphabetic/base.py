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
        if not alphabet:
            alphabet = self.DEFAULT_ALPHABET

        super().__init__(alphabet)
        self.alphabet_ = ''.join(self._transform(alphabet))
        self.xtable = OneToOneTranslationTable(self.alphabet, self.alphabet_)

    def __repr__(self):
        return '{} ({})'.format(type(self).__name__, repr(self.xtable))

    def __str__(self):
        return str(self.xtable)

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
        """ Transcode forwards.

        Parameters
        ----------
        s : str
            A string to transcode.

        Returns
        -------
        out : str
            The transcoded string output.

        """
        return self.xtable.encode(s)

    def _decode(self, s):
        """ Transcode backwards.

        Parameters
        ----------
        s : str
            A string to transcode.

        Returns
        -------
        out : str
            The transcoded string output.

        """
        return self.xtable.decode(s)
