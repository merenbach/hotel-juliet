#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import Cipher


class NullCipher(Cipher):
    """ Base class for ciphers.

    """
    verbose_name = 'null'

    def _encode(self, s):
        """ Encoding logic.

        Parameters
        ----------
        s : str
            A message to encode.

        Returns
        -------
        out : str
            An encoded message.

        """
        return s

    def _decode(self, s):
        """ Decoding logic.

        Parameters
        ----------
        s : str
            A message to decode.

        Returns
        -------
        out : str
            A decoded message.

        """
        return s
