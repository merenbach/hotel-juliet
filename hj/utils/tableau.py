#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple


class CipherTableau(namedtuple('CipherTableau', 'pt ct')):
    """ A one-to-one, bidirectional, plaintext/ciphertext translation tableau.

    Parameters
    ----------
    pt : str
        A plaintext alphabet for the tableau.
    ct : str
        A ciphertext alphabet for the tableau.

    Notes
    -----
    In a typical monoalphabetic substitution tableau, one plaintext character
    maps to one ciphertext character, and vice-versa.  _That is this class._
    No recurrences exist in either the plaintext or the ciphertext alphabet.

    In a homophonic substitution tableau, one plaintext character may
    map to multiple ciphertext characters, with several enciphered symbols
    representing certain plaintext characters so as to even out frequencies
    of letters and thereby hinder cryptanalysis.  _This could be a subclass._

    What this has in common with a polyalphabetic tableau is that in both
    cases, one plaintext character may be represented by multiple ciphertext
    characters.  In a monoalphabetic cipher, however, those ciphertext
    characters must always map back to the same plaintext character, regardless
    of key, whereas in a true polyalphabetic substitution cipher, a key will
    determine to which plaintext character a ciphertext character maps.

    """
    __slots__ = ()

    def __str__(self):
        return 'PT: {}\nCT: {}'.format(self.pt, self.ct)

    @property
    def pt2ct(self):
        """ Create a translation table from plaintext to ciphertext.

        Returns
        -------
        out : dict
            A Unicode translation dict.

        Notes
        -----
        If any individual characters appear more than once in the plaintext
        alphabet `pt`, unexpected output may occur when the table is used.

        """
        return str.maketrans(self.pt, self.ct)

    @property
    def ct2pt(self):
        """ Create a translation table from ciphertext to plaintext.

        Returns
        -------
        out : dict
            A Unicode translation dict.

        Notes
        -----
        If any individual characters appear more than once in the ciphertext
        alphabet `ct`, unexpected output may occur when the table is used.

        """
        return str.maketrans(self.ct, self.pt)
