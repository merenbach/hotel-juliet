#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import Cipher
from utils import intersect
import string


class TransCipher(Cipher):
    """ Abstract-ish base class for transposition ciphers.

    """
    DEFAULT_ALPHABET = string.ascii_uppercase

    def __init__(self, key, alphabet=None):
        self.key = key
        self.alphabet = alphabet or self.DEFAULT_ALPHABET
        super().__init__()

    def encode(self, s, block=None):
        """ Encode a message.

        Parameters
        ----------
        s : str
            A message to encode.
        block : int, optional
            Divide output into blocks of this size.  All non-transcodable
            symbols will be stripped.  Specify the value `0` to strip all
            non-transcodable symbols and not divide into blocks.
            Specify the value `None` to disable chunking.  Default `None`.

        Returns
        -------
        out : str
            The encoded message.

        Notes
        -----
        Although this can invoke either `self._encode` or `super().encode`, it
        essentially falls prey to the "call super" antipattern and should
        probably be refactored. [TODO]

        """
        if block is not None:
            # filter message to characters in ciphertext alphabet
            s = intersect(s, self.alphabet)

            if block > 0:
                padding = upward_factor(block, len(s))
                s = s.ljust(padding, self.DEFAULT_NULLCHAR)

        out = super().encode(s)

        if block is not None and block > 0:
            out = ' '.join(chunks(out, block))

        return ''.join(out)

    def decode(self, s, block=None):
        """ Decode a message.

        Parameters
        ----------
        s : str
            A message to decode.
        block : int, optional
            Divide output into blocks of this size.  All non-transcodable
            symbols will be stripped.  Specify the value `0` to strip all
            non-transcodable symbols and not divide into blocks.
            Specify the value `None` to disable chunking.  Default `None`.

        Returns
        -------
        out : str
            The decoded message.

        Notes
        -----
        Although this can invoke either `self._encode` or `super().encode`, it
        essentially falls prey to the "call super" antipattern and should
        probably be refactored. [TODO]

        """
        if block is not None:
            # filter message to characters in ciphertext alphabet
            s = intersect(s, self.alphabet)

        out = super().decode(s)

        if block is not None and block > 0:
            padding = upward_factor(block, len(out))
            out = out.ljust(padding, self.DEFAULT_NULLCHAR)
            out = ' '.join(chunks(out, block))

        return ''.join(out)
