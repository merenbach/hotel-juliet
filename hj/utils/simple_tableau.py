#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
from . import base
import itertools


class SimpleTableau(namedtuple('SimpleTableau', 'pt ct')):
    """ A one-to-one, bidirectional, plaintext/ciphertext translation table.

    Parameters
    ----------
    pt : str
        A plaintext alphabet for the tableau.
    ct : str
        A ciphertext alphabet for the tableau.

    Notes
    -----
    Unexpected results may occur if any characters recur within `pt` or `ct`.
    At most any character should occur just once in `pt` and once in `ct`.

    One notable feature of this class is its use of `str.maketrans()` and
    `str.translate()`.  This is perfect for many common substitution ciphers
    (both monoalphabetic and polyalphabetic).  Where it falls short is for more
    complicated (not necessarily more secure) substitution ciphers, such as
    those using the Polybius square, where letters may be translated into
    groups of other characters (e.g., pairs of digits).  Meanwhile, on both the
    plaintext and ciphertext sides, dividing up the source or destination
    message into digraphs or trigraphs again becomes easier when your tableau
    can treat groups of characters as one logical unit.

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

    [TODO] this needs direct unit tests

    """
    __slots__ = ()

    def __str__(self):
        return 'PT: {}\nCT: {}'.format(self.pt, self.ct)

    @staticmethod
    def translate(e, src, dst, transform=None):
        """ Another way?

        Parameters
        ----------
        e : object
            An element to transform.
        src : sequence
            A source sequence.
        dst : sequence
            A destination sequence.
        transform : callable, optional
            If supplied, a callable to do additional transforms.

        Returns
        -------
        out : object
            The similarly-positioned counterpart in `dst` of `e` in `src`.

        Raises
        ------
        ValueError
            If `e` is not in `src`.
        IndexError
            If `dst` contains no elements.

        Notes
        -----
        No checking is done on the lengths of `src` and `dst`.  If they differ
        or if `src` has repeated elements, the results may not be as expected.

        This is almost equivalent to `dict(zip(src, dst))[e]`, with the
        added caveat of applying the optional `transform` callable.

        """
        pos = src.index(e)
        if callable(transform):
            pos = transform(pos)
        return dst[pos % len(dst)]

    def pt2ct(self, e, offset=0):
        """ Encipher a single element.

        Parameters
        ----------
        e : object
            An element to convert from plaintext to ciphertext.
        offset : int, optional
            If supplied, an offset to add.  Default `0`.

        Returns
        -------
        out : object
            The enciphered element, if possible.

        Raises
        ------
        ValueError
            If `e` is not in the plaintext alphabet.
        IndexError
            If the ciphertext alphabet is empty.

        Notes
        -----
        If any individual characters appear more than once in the plaintext
        alphabet `pt`, unexpected output may occur when the table is used.

        [TODO] Repeatedly calling this could prove inefficient at scale.

        """
        return self.translate(e, self.pt, self.ct, lambda x: x + offset)

    def ct2pt(self, e, offset=0):
        """ Decipher a single element.

        Parameters
        ----------
        e : object
            An element to convert from ciphertext to plaintext.
        offset : int, optional
            If supplied, an offset to subtract.  Default `0`.

        Returns
        -------
        out : object
            The enciphered element, if possible.

        Raises
        ------
        ValueError
            If `e` is not in the ciphertext alphabet.
        IndexError
            If the plaintext alphabet is empty.

        Notes
        -----
        If any individual characters appear more than once in the ciphertext
        alphabet `ct`, unexpected output may occur when the table is used.

        [TODO] Repeatedly calling this could prove inefficient at scale.

        """
        return self.translate(e, self.ct, self.pt, lambda x: x - offset)
