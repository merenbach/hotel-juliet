#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from collections import OrderedDict
from utils import TwoWayTranslationTable


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str
        A plaintext alphabet.

    """
    verbose_name = 'monoalphabetic substitution'

    def __init__(self, alphabet):
        if not alphabet:
            alphabet = self.DEFAULT_ALPHABET

        super().__init__(alphabet)
        self.alphabet_ = ''.join(self._transform(alphabet))
        self.xtable = TwoWayTranslationTable(self.alphabet, self.alphabet_)

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

    def __str__(self):
        base = super().__str__()
        pt = 'PT: {}'.format(self.alphabet)
        ct = 'CT: {}'.format(self.alphabet_)
        return '{}\n  {}\n  {}'.format(base, pt, ct)

    def __repr__(self):
        return '{}: {} <=> {}'.format(self.__class__.__name__,
                                               repr(self.alphabet),
                                               repr(self.alphabet_))

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
