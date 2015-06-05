#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import OneDimensionalTableau


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str
        A source character set to use for transcoding.
    alphabet_ : str
        A destination character set to use for transcoding.

    """
    def __init__(self, alphabet, alphabet_):
        super().__init__(alphabet)
        self.tableau = OneDimensionalTableau(alphabet, alphabet_)

    def _transform(self, alphabet):
        """ Transform a character set for transcoding.

        Parameters
        ----------
        alphabet : str
            A character set to use for transcoding.

        Returns
        -------
        out : str
            A transformed version of the provided character set.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError

    def _encode(self, s, strict):
        return [self.tableau.encode(c, strict) for c in s]

    def _decode(self, s, strict):
        return [self.tableau.decode(c, strict) for c in s]
