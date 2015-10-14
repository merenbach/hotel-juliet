#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class Cipher:
    """ Base class for ciphers.

    """
    verbose_name = 'cipher'

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

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError

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

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError

    def encode(self, s):
        """ Encode a message.

        Parameters
        ----------
        s : str
            A message to encode.

        Returns
        -------
        out : str
            The encoded message.

        """
        out = self._encode(s)
        return ''.join(out)

    def decode(self, s):
        """ Decode a message.

        Parameters
        ----------
        s : str
            A message to decode.

        Returns
        -------
        out : str
            The decoded message.

        """
        out = self._decode(s)
        return ''.join(out)
