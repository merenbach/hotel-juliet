#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import OneDimensionalTableau


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    """
    def _make_tableau(self, alphabet):
        alphabet_ = self._transform(alphabet)
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

    def _encode(self, s):
        return self.tableau.encode(s)

    def _decode(self, s):
        return self.tableau.decode(s)
