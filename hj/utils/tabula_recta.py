#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import lrotated, orotated
from .tableau import CipherTableau
from collections import OrderedDict, namedtuple


class TabulaRecta:
    """ Similar to CipherTableau, but oh-so-different.

    Parameters
    ----------
    pt : str
        A plaintext alphabet for the tableau.
    ct : str, optional
        A ciphertext alphabet for the tableau.  Defaults to `pt`.
    keys : iterable, optional
        An ordered sequence of keys to use for rows.

    """
    def __init__(self, pt, ct=None, keys=None):
        if not ct:
            ct = pt
        if not keys:
            keys = ct
        self.pt, self.ct, self.keys = pt, ct, keys # [TODO] temporary?
        makerows = [lrotated(ct, i) for i in range(len(keys))]
        tableaux = [CipherTableau(pt, ct_) for ct_ in makerows]
        self.rows = OrderedDict(zip(keys, tableaux))


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
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    alphabet : str
        An alphabet for the tableau.  Duplicate elements will be removed.
    keys : iterable, optional
        An ordered sequence of keys to use for rows.

    """
    def __init__(self, pt, alphabet_=None, keys=None):
        super().__init__(pt, alphabet_ or pt)
        alphabets_ = self._make_rows(pt)
        # transcoders_list = [CaesarCipher(n, alphabet=alphabet)
        #                     for n, __ in enumerate(alphabet)]
        self.keys = keys or pt
        self.key_table = OrderedDict(zip(keys or pt, alphabets_))
        self.rows = OrderedDict(zip(keys or alphabet_ or pt, alphabets_))

    def __repr__(self):
        return '{}: PT=[{}], CT=[{}], keys=[{}]'.format(type(self).__name__,
                                      repr(self.pt),
                                      repr(self.ct),
                                      ''.join(self.key_table.keys()))

    def encipher(self, element, key):
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
        ValueError
            If no tableau could be found for the given key.

        """
        if element not in self.pt:
            raise ValueError
        return self.key_table[key].encipher(element)

    def decipher(self, element, key):
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
        ValueError
            If no tableau could be found for the given key.

        """
        if element not in self.ct:
            raise ValueError
        return self.key_table[key].decipher(element)

    def __str__(self):
        alphabet = self.pt
        lines = []
        lines.append('  | ' + ' '.join(alphabet))
        lines.append('--+' + '-' * len(alphabet) * 2)
        for k, v in self.key_table.items():
            row = ' '.join(v.ct)
            lines.append('{0} | {1}'.format(k, row))
        return '\n'.join(lines)

    def _make_rows(self, alphabet):
        """ Create alphabets.

        Returns
        -------
        out : list
            An ordered collection of character sets.

        """
        cts = [lrotated(self.ct, i) for i, _ in enumerate(self.ct)]
        return [CipherTableau(self.pt, ct) for ct in cts]



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
        alphabet = self.pt[:len(self.alphabet) // 2]
        lines = []
        lines.append('     | ' + ' '.join(alphabet))
        lines.append('-----+' + '-' * len(alphabet) * 2)
        cur_header = None
        for i, (k, v) in enumerate(self.key_table.items()):
            if i % 2 == 0:
                cur_header = k
            elif i % 2 == 1:
                row = ' '.join(v.alphabet_[:len(alphabet)])
                lines.append('{0}, {1} | {2}'.format(cur_header, k, row))
        return '\n'.join(lines)

    def _make_rows(self, alphabet):
        alphabet2 = lrotated(self.pt, len(self.pt) // 2)
        cts = [orotated(alphabet2, i // 2) for i in range(len(self.pt))]
        return [CipherTableau(self.pt, ct) for ct in cts]


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
