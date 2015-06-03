#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import OneDimensionalTableau


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    transform : callable
        A function with one positional parameter to transform an alphabet.
    alphabet : str, optional
        A character set to use for transcoding.  Default `None`.

    """
    def __init__(self, transform, alphabet=None):
        self.transform = transform
        super().__init__(alphabet)

    def _make_tableau(self, alphabet):
        alphabet_ = self.transform(alphabet)
        return OneDimensionalTableau(alphabet, alphabet_)

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
        return self.tableau.encode(s, strict=strict)

    def _decode(self, s, strict):
        return self.tableau.decode(s, strict=strict)
