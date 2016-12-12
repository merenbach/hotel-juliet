#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import Alphabet
from utils import SimpleTableau


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    """
    def __init__(self, key, alphabet=None):
        super().__init__()

        alphabet = Alphabet(alphabet)
        alphabet_ = self.transform(alphabet, key)
        self.tableau = SimpleTableau(alphabet, alphabet_)

    def _encode(self, s):
        """ Encode a message.

        Parameters
        ----------
        s : str
            A message to transcode.

        Yields
        ------
        out : str
            A transcoded version of `s`.

        Notes
        -----
        A subclass needing more specialized behavior (e.g., a homophonic
        substitution cipher) should override this and customize as needed.

        """
        for c in s:
            try:
                yield self.tableau.pt2ct(c)
            except ValueError:
                yield c

    def _decode(self, s):
        """ Decode a message.

        Parameters
        ----------
        s : str
            A message to transcode.

        Yields
        ------
        out : str
            A transcoded version of `s`.

        Notes
        -----
        A subclass needing more specialized behavior (e.g., a homophonic
        substitution cipher) should override this and customize as needed.

        """
        for c in s:
            try:
                yield self.tableau.ct2pt(c)
            except ValueError:
                yield c
