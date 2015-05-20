#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import Alphabet, TabulaRecta


class PolySubCipher(SubCipher):
    """ A representation of a tabula recta cipher

    Parameters
    ----------
    alphabet : str or string like, optional
        An alphabet to use for transcoding.  Default `None`.

    """
    def __init__(self, alphabet=None):
        alphabet = Alphabet(alphabet)
        tableau = self._make_tableau(alphabet)
        super().__init__(tableau)

    def _make_tableau(self, alphabet):
        """ Create a tabula recta for transcoding.

        Parameters
        ----------
        alphabet : sequence
            An alphabet to use for transcoding.

        Returns
        -------
        out : utils.tableau.TabulaRecta
            A tabula recta to use for transcoding.

        Notes
        -----
        Since this is invoked by `__init__()` before instance is totally
        initialized, please don't perform any operations that expect a fully
        constructed instance.

        """
        return TabulaRecta(alphabet=alphabet)

    def _encode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        if strict:
            s = ''.join(c for c in s if c in self.tableau.alphabet)
        return self._transcode(s, reverse=False)

    def _decode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        if strict:
            s = ''.join(c for c in s if c in self.tableau.alphabet)
        return self._transcode(s, reverse=True)

    def _transcode(self, s, reverse=False):
        raise NotImplementedError
