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
        self.transcoder = Transcoder(alphabet, alphabet_)
        super().__init__()

    def __repr__(self):
        return repr(self.transcoder)

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
        raise NotImplementedError

    def _encode(self, s, strict):
        return self.transcoder.encode(s, strict=strict)

    def _decode(self, s, strict):
        return self.transcoder.decode(s, strict=strict)
