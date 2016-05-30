#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import base
from .simple_tableau import SimpleTableau
from collections import OrderedDict


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
        self.pt, self.ct = pt, ct or pt
        self.rows = OrderedDict(self.tableaux(pt, ct or pt, keys or ct or pt))

    @staticmethod
    def tableaux(pt, ct, keys):
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
        for i, k in enumerate(keys):
            yield (k, SimpleTableau(pt, base.lrotated(ct, i)))

    def __str__(self):
        lines = []
        lines.append('  | ' + ' '.join(self.pt))
        lines.append('--+' + '-' * len(self.pt) * 2)
        for k, v in self.rows.items():
            line = '{} | {}'.format(k, ' '.join(v.ct))
            lines.append(line)
        return '\n'.join(lines)

    # def __repr__(self):
    #     pass


class ReciprocalTable(TabulaRecta):
    """ Message alphabet is on top; key alphabet is on side.  This class doesn't
    serve much purpose right now, but that may change.

    Parameters
    ----------
    alphabet : str
        An alphabet for the tableau.  Duplicate elements will be removed.
    keys : iterable, optional
        An ordered sequence of keys to use for rows.

    """
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
        for i, (k, v) in enumerate(self.rows.items()):
            if i % 2 == 0:
                cur_header = k
            elif i % 2 == 1:
                row = ' '.join(v.ct[:len(alphabet)])
                lines.append('{0}, {1} | {2}'.format(cur_header, k, row))
        return '\n'.join(lines)

    @staticmethod
    def tableaux(pt, ct, keys):
        ct_ = base.lrotated(pt, len(pt) // 2)
        for i, k in enumerate(keys):
            yield (k, SimpleTableau(pt, base.orotated(ct_, i // 2)))


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
