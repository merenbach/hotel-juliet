#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import base
from .alphabet import Alphabet
from .simple_tableau import SimpleTableau
from collections import OrderedDict

# class TR2:
#     """ Curious proof-of-concept for a tabula recta using only modular
#     arithmetic.  Presumably will scale better with larger alphabets (e.g.,
#     3500x3500).  Also of note is that it has its own encode/decode for
#     individual characters.

#     Notes
#     -----
#     Intriguingly, multiple keys may be used in one fell swoop here if they are
#     summed into a single value.

#     """
#     def __init__(self, pt, ct, keys):
#         self.t = SimpleTableau(pt, ct or pt)
#         self.keys = keys

#     def encode(self, pt, k):
#         pos_p = self.t.pt.index(pt)
#         pos_k = self.keys.index(k)
#         o = (pos_p + pos_k) % len(self.t.ct)
#         return self.t.ct[o]

#     def decode(self, ct, k):
#         pos_c = self.t.ct.index(ct)
#         pos_k = self.keys.index(k)
#         o = (pos_c - pos_k) % len(self.t.pt)
#         return self.t.pt[o]


class TabulaRecta:
    """ A two-dimensional, rectangular grid for polyalphabetic transcoding.

    Parameters
    ----------
    pt : str
        A plaintext alphabet for the tableau.
    ct : str, optional
        A ciphertext alphabet for the tableau.  Defaults to `pt`.
    keys : iterable, optional
        An ordered sequence of keys to use for rows.  Defaults to `ct`.

    """
    def __init__(self, pt, ct=None, keys=None):
        pt, ct, keys = Alphabet(pt), Alphabet(ct), Alphabet(keys)

        self.pt, self.ct = pt, ct
        self.tableau = SimpleTableau(pt, ct)
        self.keys = keys

    # def __repr__(self):
    #     pass

    def __str__(self):
        lines = []
        lines.append('  | ' + ' '.join(self.tableau.pt))
        lines.append('--+' + '-' * len(self.tableau.pt) * 2)
        for k in self.keys:
            changed = [self.tableau.pt2ct(e, k) for e in self.tableau.ct]
            line = '{} | {}'.format(k, ' '.join(changed))
            lines.append(line)
        return '\n'.join(lines)

    def pt2ct(self, e, key):
        """ Create a translation table from plaintext to ciphertext.

        Parameters
        ----------
        e : object
            An element to convert from plaintext to ciphertext.
        key : object
            A key to use.

        Returns
        -------
        out : object
            The transcoded character.

        """
        k = self.keys.index(key)
        return self.tableau.pt2ct(e, k)

    def ct2pt(self, e, key):
        """ Create a translation table from plaintext to ciphertext.

        Parameters
        ----------
        e : object
            An element to convert from ciphertext to plaintext.
        key : object
            A key to use.

        Returns
        -------
        out : object
            The transcoded character.

        """
        k = self.keys.index(key)
        return self.tableau.ct2pt(e, k)


class ReciprocalTable:
    """ Message alphabet is on top; key alphabet is on side.  This class doesn't
    serve much purpose right now, but that may change.

    Parameters
    ----------
    alphabet : str
        An alphabet for the tableau.  Duplicate elements will be removed.
    keys : iterable, optional
        An ordered sequence of keys to use for rows.

    """
    def __init__(self, pt, ct=None, keys=None):
        pt, ct = Alphabet(pt), Alphabet(ct or pt)
        keys = Alphabet(keys)
        self.pt, self.ct = pt, ct
        self.rows = OrderedDict(zip(keys, self.tableaux(pt, ct)))
        self.keys = keys

    @staticmethod
    def tableaux(pt, ct):
        """ Generate all the needed cipher tableaux.

        Parameters
        ----------
        pt : str
            A plaintext alphabet for the tableaux.
        ct : str
            A ciphertext alphabet for the tableaux.
        keys : iterable
            An ordered sequence of keys to use for rows.

        Yields
        ------
        out : tuple
            A tuple in format (key character, cipher tableau).

        """
        from itertools import count
        for i in count():
            ct_ = Alphabet(base.lrotated(ct, i))
            yield SimpleTableau(pt, ct_)

    def __repr__(self):
        return '{}: PT=[{}], CT=[{}], keys=[{}]'.format(type(self).__name__,
                                      repr(self.pt),
                                      repr(self.ct),
                                      ''.join(self.key_table.keys()))

    def __str__(self):
        alphabet = self.pt
        lines = []
        lines.append('  | ' + ' '.join(alphabet))
        lines.append('--+' + '-' * len(alphabet) * 2)
        for k, v in self.key_table.items():
            row = ' '.join(v.ct)
            lines.append('{0} | {1}'.format(k, row))
        return '\n'.join(lines)

    def pt2ct(self, e, key):
        """ Create a translation table from plaintext to ciphertext.

        Parameters
        ----------
        e : object
            An element to convert from plaintext to ciphertext.
        key : object
            A key to use.

        Returns
        -------
        out : object
            The transcoded character.

        """
        return self.rows[key].pt2ct(e)

    def ct2pt(self, e, key):
        """ Create a translation table from plaintext to ciphertext.

        Parameters
        ----------
        e : object
            An element to convert from ciphertext to plaintext.
        key : object
            A key to use.

        Returns
        -------
        out : object
            The transcoded character.

        """
        return self.rows[key].ct2pt(e)


# TODO: this is actually a reciprocal table...
class DellaPortaTabulaRecta(ReciprocalTable):
    """ Porta cipher version, doubling up rows and symmetrically rotating.

    [TODO] Would like to be able to make fewer overrides on parent class logic,
    as well as more nicely represent the tableau in __repr__, say with
    either collapsed rows... or with keys equal to
    [('A', 'B'), ('C', 'D'), ... ('Y', 'Z')] and a "search" function
    to find the right one before passing to super.

    """
    def __str__(self):
        alphabet = self.pt[:len(self.pt) // 2]
        lines = []
        lines.append('     | ' + ' '.join(alphabet))
        lines.append('-----+' + '-' * len(alphabet) * 2)
        cur_header = None
        for i, (k, v) in enumerate(self.items()):
            if i % 2 == 0:
                cur_header = k
            elif i % 2 == 1:
                row = ' '.join(v.ct[:len(alphabet)])
                lines.append('{0}, {1} | {2}'.format(cur_header, k, row))
        return '\n'.join(lines)

    @staticmethod
    def tableaux(pt, ct):
        ct = base.lrotated(pt, len(pt) // 2)
        from itertools import count
        for i in count():
            ct_ = (base.orotated(ct, i // 2))
            yield SimpleTableau(pt, ct_)
        # while True:
        #     ct = ct.lrotated(1)
        #     yield SimpleTableau(pt, ct)


# class PolybiusSquare(Tableau):
### [TODO] the hardest part here will be textual representation, e.g. __str__,
### as the polybius square is going to be a substitution cipher where pairs of
### digits map to symbols (e.g., 12 => BAT).  Actually, perhaps the hardest
### part will be filtering out I/J in a 5x5 grid one way, but translating to
### only one or the other in reverse.
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
