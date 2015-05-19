#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils.alphabet import Alphabet
from utils.transcoder import Transcoder


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str or string like, optional
        A source (plaintext) alphabet to underlie transcoding.  Default `None`.
        If you cannot afford one, one will
        be provided for you at no cost to you.

    Raises
    ------
    ValueError
        If `alphabet` and `alphabet_` have unequal length.

    """
    def __init__(self, alphabet):
        alphabet = Alphabet(alphabet)
        alphabet_ = self.make_alphabet_(alphabet)
        tableau = Transcoder(alphabet, alphabet_)
        super().__init__(tableau)

    def make_alphabet_(self, alphabet):
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
        # [TODO] change to maketranscoders a la poly ciphers?
        raise NotImplementedError

    def _encode(self, s, strict):
        if strict:
            s = self.tableau.sanitize(s)
        return self.tableau.encode(s)

    def _decode(self, s, strict):
        if strict:
            s = self.tableau.sanitize(s)
        return self.tableau.decode(s)
