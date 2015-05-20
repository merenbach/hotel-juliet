#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils.alphabet import Alphabet
from utils.transcoder import Transcoder


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    charset : str
        A character set to use for transcoding.

    """
    def __init__(self, charset):
        alphabet = Alphabet(charset)
        alphabet_ = self._make_alphabet(alphabet)
        tableau = Transcoder(alphabet, alphabet_)
        super().__init__(tableau)

    def _make_alphabet(self, alphabet):
        """ Create a transcoding alphabet.

        Parameters
        ----------
        alphabet : sequence
            An alphabet to transform.

        Returns
        -------
        out : sequence
            A transformed alphabet.

        Raises
        ------
        NotImplementedError
            If not overridden.

        Notes
        -----
        Since this is invoked by `__init__()` before instance is totally
        initialized, please don't perform any operations that expect a fully
        constructed instance.

        """
        raise NotImplementedError

    def _encode(self, s, strict):
        if strict:
            s = self.tableau.sanitize(s)
        return self.tableau.encode(s)

    def _decode(self, s, strict):
        if strict:
            s = self.tableau.sanitize(s)
        return self.tableau.decode(s)
