#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from collections import OrderedDict


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str
        A plaintext alphabet.

    """
    verbose_name = 'monoalphabetic substitution'

    def __init__(self, alphabet):
        super().__init__(alphabet)

    def alphabet_(self):
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

    def __str__(self):
        base = super().__str__()
        pt = 'PT: {}'.format(self.alphabet)
        ct = 'CT: {}'.format(self.alphabet_())
        return '{}\n  {}\n  {}'.format(base, pt, ct)

    def __repr__(self):
        return '{}: {} <=> {}'.format(self.__class__.__name__,
                                               repr(self.alphabet),
                                               repr(self.alphabet_()))

    def _encode(self, s):
        """ Transcode forwards.

        Parameters
        ----------
        s : iterable
            An iterable of elements to transcode.

        Returns
        -------
        out : generator
            The transcoded counterparts, if possible, of the input sequence.

        """
        xtable = str.maketrans(self.alphabet, self.alphabet_())
        return s.translate(xtable)

    def _decode(self, s):
        """ Transcode backwards.

        Parameters
        ----------
        s : iterable
            An iterable of elements to transcode.

        Returns
        -------
        out : generator
            The transcoded counterparts, if possible, of the input sequence.

        """
        xtable = str.maketrans(self.alphabet_(), self.alphabet)
        return s.translate(xtable)
