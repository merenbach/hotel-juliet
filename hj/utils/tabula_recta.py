#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import lrotated, orotated
from collections import OrderedDict
from string import digits
from ciphers.substitution.monoalphabetic import MonoSubCipher
from ciphers.substitution.monoalphabetic import CaesarCipher

# [TODO] some way to match up transcodeable chars + usable key chars?
#
#   OCEANOGRAPHYWHAT!ILOVEund4Da$eA
#   STORM THE CASTLE AT MIDNIGHT
#
# to
#
#   OCEAN#OGR#APHYWH#AT#!I LOVEund4Da$eA
#   STORM THE CASTLE AT #MIDNIG####H###T

class TabulaRecta:
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    alphabet : str
        An alphabet for the tableau.  Duplicate elements will be removed.
    keys : iterable, optional
        An ordered sequence of keys to use for rows.

    """
    def __init__(self, alphabet, keys=None):
        self.alphabet = alphabet
        self.keys = keys or alphabet
        alphabets_ = self._make_rows(alphabet)
        self.alphabets_ = alphabets_
        # transcoders_list = [CaesarCipher(n, alphabet=alphabet)
        #                     for n, __ in enumerate(alphabet)]
        self.key_table = OrderedDict(zip(keys or alphabet, alphabets_))

    def encode(self, seq, key):
        """ Locate element within the grid.

        Parameters
        ----------
        element : str
            An element to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.

        Returns
        -------
        out : data-type
            A transcoded copy (if possible) of the given element `element`.

        Raises
        ------
        KeyError
            If no tableau could be found for the given key.

        """
        return self.key_table[key].encode(seq, strict=True)

    def decode(self, seq, key):
        """ Locate element within the grid.

        Parameters
        ----------
        element : str
            An element to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.

        Returns
        -------
        out : data-type
            A transcoded copy (if possible) of the given element `element`.

        Raises
        ------
        KeyError
            If no tableau could be found for the given key.

        """
        return self.key_table[key].decode(seq, strict=True)

    def __str__(self):
        alphabet = self.alphabet
        lines = []
        lines.append('  | ' + ' '.join(alphabet))
        lines.append('--+' + '-' * len(alphabet) * 2)
        for k, v in zip(self.keys or alphabet, self.alphabets_):
            row = ' '.join(v.a2b.xtable.values())
            lines.append('{0} | {1}'.format(k, row))
        return '\n'.join(lines)

    def _make_rows(self, alphabet):
        """ Create alphabets.

        Returns
        -------
        out : list
            An ordered collection of character sets.

        """
        # abets = [lrotated(alphabet, i) for i in range(len(alphabet))]
        # return [MonoSubCipher(alphabet, alphabet_) for alphabet_ in abets]
        # return [lrotated(alphabet, i) for i, _ in enumerate(alphabet)]
        return [CaesarCipher(i, alphabet=alphabet) for i in
                range(len(alphabet))]


class GronsfeldTabulaRecta(TabulaRecta):
    """ Gronsfeld cipher version.

    Parameters
    ----------
    alphabet : str
        An alphabet to use for this tabula recta.

    """
    def __init__(self, alphabet):
        super().__init__(alphabet, keys=digits)


class BeaufortTabulaRecta(TabulaRecta):
    """ Beaufort cipher version.

    Parameters
    ----------
    alphabet : str
        An alphabet to use for this tabula recta.

    """
    def __init__(self, alphabet):
        super().__init__(alphabet, keys=(alphabet[::-1]))

    def _make_rows(self, alphabet):
        # abets = [lrotated(alphabet, i) for i in range(len(alphabet))]
        # n = super()._make_rows(alphabet[::-1])
        # print(n)
        # return n
        # return list(reversed(n))
        abets = [lrotated(alphabet[::-1], i) for i in range(len(alphabet))]
        return [MonoSubCipher(alphabet, alphabet_) for alphabet_ in abets]
        # return [AtbashCipher(alphabet=alphabet) for i, __ in enumerate(alphabet)]


# TODO: this is actually a reciprocal table...
class DellaPortaTabulaRecta(TabulaRecta):
    """ Porta cipher version, doubling up rows and symmetrically rotating.

    [TODO] Would like to be able to make fewer overrides on parent class logic,
    as well as more nicely represent the tableau in __repr__, say with
    either collapsed rows... or with keys equal to
    [('A', 'B'), ('C', 'D'), ... ('Y', 'Z')] and a "search" function
    to find the right one before passing to super.

    """
    def __str__(self):
        alphabet = self.alphabet[:len(self.alphabet) // 2]
        lines = []
        lines.append('     | ' + ' '.join(alphabet))
        lines.append('-----+' + '-' * len(alphabet) * 2)
        cur_header = None
        for i, (k, v) in enumerate(self.alphabets_.items()):
            if i % 2 == 0:
                cur_header = k
            elif i % 2 == 1:
                row = ' '.join(v.alphabet_[:len(alphabet)])
                lines.append('{0}, {1} | {2}'.format(cur_header, k, row))
        return '\n'.join(lines)

    def _make_rows(self, alphabet):
        alphabet2 = lrotated(alphabet, len(alphabet) // 2)
        abets = [orotated(alphabet2, i // 2) for i in range(len(alphabet))]
        return [MonoSubCipher(alphabet, alphabet_) for alphabet_ in abets]


    #
    #     # [TODO] kludgy vars that shouldn't be here
    #     # self.msg_alphabet = alphabet
    #     # self.keys = alphabet
    #
    #     # try:
    #     #     x, y = self.charmap[a], self.charmap[b]
    #     # except KeyError:
    #     #     return None
    #     # else:
    #     #     pos = x + y if intersect else x - y
    #     #     element = self.alphabet.at(pos)
    #     #     return str(element)
    #
    # def _make_transcoders(self):
    #     """ [TODO] these docs aren't current
    #     Create a transcoding alphabet.
    #
    #     Returns
    #     -------
    #     out : sequence
    #         A transformed alphabet.
    #
    #     Raises
    #     ------
    #     NotImplementedError
    #         If not overridden.
    #
    #     Notes
    #     -----
    #     Since this is invoked by `__init__()` before instance is totally
    #     initialized, please don't perform any operations that expect a fully
    #     constructed instance.
    #
    #     """
    #     raise NotImplementedError

# class PolybiusSquare(Tableau):
#     # alphabet = ascii_uppercase
#     DEFAULT_OVERLAP = {'J': 'I'}
#     DEFAULT_NULLCHAR = 'X'
#
#     def __init__(self, alphabet=None, keys=None):
#         from string import ascii_uppercase
#         from .base import unique, grouper
#         alphabet = ''.join(unique(alphabet or ascii_uppercase))
#         keys = ''.join(unique(keys or '12345'))
#         self.alphabet, self.keys = alphabet, keys
#         rowlists = grouper(alphabet, len(keys), fillvalue=self.DEFAULT_NULLCHAR)
#         rows = [OrderedDict(zip(keys, rowlist)) for rowlist in rowlists]
#         super().__init__(rows)
#
#     def get(self, row, col):
#         transcoder = self.alphabets_.get(row)
#         return transcoder and transcoder.get(col)
#
#     def __repr__(self):
#         alphabet = self.alphabet
#         lines = []
#         lines.append('  | ' + ' '.join(str(i) for i in self.keys))
#         lines.append('--+' + '-' * len(alphabet) * 2)
#         for k, v in self.alphabets_.items():
#             row = ' '.join(v.values())
#             lines.append('{0} | {1}'.format(k, row))
#         return '\n'.join(lines)

#from utils.alphabet import Alphabet
#
## def yielder(alphabet, keybet=None):
##     max_alphas = len(keybet or alphabet)
##     for n in range(max_alphas)
##         yield alphabet.lrotate(n)
#
#from .alphabet import BaseAlphabetTranscoder
#
#
#class BaseTabulaRecta(BaseAlphabetTranscoder):
#    """ 
#
#    Parameters
#    ----------
#    alphabet : str or string like
#        An alphabet to use.
#    alphabet_ : str or string like, optional
#        An alternative alphabet to use for keying.
#
#    """
#    def __init__(self, alphabet, alphabet_=None):
#        super().__init__(alphabet, alphabet_ or alphabet)
#
#
#class TabulaRecta(BaseTabulaRecta):
#    """ Message alphabet is on top; key alphabet is on side.
#
#    Parameters
#    ----------
#    alphabet : str or string like
#        An alphabet to use.  Message encoding will occur with this alphabet.
#        The message and this alphabet must have overlapping character sets.
#    alphabet_ : str or string like
#        A cipher alphabet to use.  Passphrase keying will occur with this
#        alphabet.  The passphrase and this alphabet must have overlapping
#        character sets.
#
#    Notes
#    -----
#    Since (en/de)ciphering is done positionally with math, it really doesn't
#    matter whether the two alphabets are the same length or even whether
#    they have any of the same characters.
#
#    As long as the passphrase (in the polyalphabetic cipher) and the alphabet
#    passed in have the same character set (or rather, provided that the
#    key alphabet is a superset of the passphrase character set), everything
#    will translate fine.  Random Unicode glyphs could be used.
#
#    """
#    def __init__(self, alphabet=None, alphabet_=None):
#        super().__init__(alphabet, alphabet_)
#        # [TODO] kludgy vars that shouldn't be here
#        self.msg_alphabet = self.alphabet
#        self.key_alphabet = self.alphabet_
#
#    def intersect(self, col_char, row_char):
#        """ Locate character within the grid.
#
#        Parameters
#        ----------
#        col : str or string like
#            The header character of the column to use.
#        row : str or string like
#            The header character of the row to use.
#
#        Returns
#        -------
#        out : str
#            The element at the intersection of column `col` and row `row`.
#
#        Notes
#        -----
#        Order of params is not important here _except_ insofar as
#        the tabula recta may not be square (e.g., Gronsfeld cipher).
#
#        """
#        try:
#            m = self.alphabet.index(str(col_char))
#            k = self.alphabet_.index(str(row_char))
#        except ValueError:
#            return None
#        else:
#            idx = (m+k) % len(self.alphabet)
#            out = self.alphabet[idx]
#            return str(out)
#
#    def locate(self, col_char, row_char):
#        """ Locate character at intersection of character `a` with row occupant character `k` """
#        """ Order here *is* important, but has nothing to do with rows vs. columns """
#        """ If character `a` not found, return None
#
#        Returns
#        -------
#        out : str
#            The element (encoded or plaintext) that intersects with
#            edge character `msg_char` to find character `key_char`.
#
#        """
#        try:
#            m = self.alphabet.index(str(col_char))
#            k = self.alphabet_.index(str(row_char))
#        except KeyError:
#            return None
#        else:
#            idx = (m-k) % len(self.alphabet)
#            out = self.alphabet[idx]
#            return str(out)
#
#    # def __repr__(self):
#    #     rows = ['    ' + ' '.join(str(self.alphabet))]
#    #     rows.append('  +' + '-' * 2 * len(self.alphabet))
#    #     rows.extend([str(row[0]) + ' | ' + ' '.join(str(row)) for row in self.rows])
#    #     return '\n'.join(rows)
#
#
#
#    #def p(self, delimiter=' '):
#    #    rows = []
#    #    l = len(self.table[0].elements)
#    #    rows.append(delimiter * 4 + delimiter.join(self.table[0].elements))
#    #    rows.append(delimiter * 2 + '+' + '-' * (l * 2))
#    #    rows.extend(row.elements[0] + ' |' + delimiter + delimiter.join(row.elements) for row in self.table)
#    #    return '\n'.join(rows)
#
## class BeaufortTabulaRecta(TabulaRecta):
##     """ Message alphabet is on top; key alphabet is on side.
##
##     Parameters
##     ----------
##     alphabet : str or string like, optional
##         An alphabet to use for transcoding.
##
##     """
##     def _make_alphabets(self, alphabet):
##         """ Create alphabets.
##
##         """
##         return super()._make_alphabets(~alphabet[::-1])
##         transcoders = []
##         for i, c in enumerate(alphabet):
##             alphabet_ = alphabet.lrotate(i)
##             transcoders.append(Transcoder(alphabet, alphabet_[::-1]))
##         return transcoders
##
##
##
##
