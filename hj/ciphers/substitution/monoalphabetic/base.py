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

    def _encode(self, s, block):
        """ Encode a message.

        Parameters
        ----------
        s : str
            A message to transcode.
        block : int or None
            Divide output into blocks of this size.  All non-transcodable
            symbols will be stripped.  Specify the value `0` to strip all
            non-transcodable symbols and not divide into blocks.
            Specify the value `None` to disable chunking.

        Returns
        -------
        out : str
            A transcoded version of `s`.

        """
        return self.xtable.encode(s, block=block)

    def _decode(self, s, block):
        """ Decode a message.

        Parameters
        ----------
        s : str
            A message to transcode.
        block : int or None
            Divide output into blocks of this size.  All non-transcodable
            symbols will be stripped.  Specify the value `0` to strip all
            non-transcodable symbols and not divide into blocks.
            Specify the value `None` to disable chunking.

        Returns
        -------
        out : str
            A transcoded version of `s`.

        """
        return self.xtable.decode(s, block=block)
