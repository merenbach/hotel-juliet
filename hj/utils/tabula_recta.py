#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .alphabet import Alphabet, BaseTabula
from .base import index_map


class TabulaRecta(BaseTabula):
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    alphabet : str or string like, optional
        An alphabet to use for transcoding.

    """
    def __init__(self, alphabet=None):
        super().__init__(alphabet)
        self.charmap = index_map(self.alphabet)

        # [TODO] kludgy vars that shouldn't be here
        self.msg_alphabet = self.alphabet
        self.key_alphabet = self.alphabet

    def transcode(self, m, k, intersect=False):
        """ Locate character within the grid.

        Parameters
        ----------
        m : str
            A character in the message alphabet.
        k : str
            A character in the key alphabet.
        intersect : bool, optional
            `True` to find character at intersection of `k` and `m`.
            `False` to work back from `k` and intersection `m` to find edge.
            Default `False`.

        Returns
        -------
        out : str
            The transcoded character in the message alphabet.

        """
        try:
            i, j = self.charmap[m], self.charmap[k]
            if not intersect:
                j *= (-1)
        except KeyError:
            return None
        else:
            pos = (i + j) % len(self.alphabet)
            element = self.alphabet[pos]
            return str(element)

    def __repr__(self):
        alphabet = self.alphabet

        rows = [self.alphabet << n for n in range(len(alphabet))]
        keyed_rows = dict(zip(self.alphabet_, rows))
        lines = []
        lines.append('    ' + ' '.join(str(alphabet)))
        lines.append('')

        for k in self.alphabet_:
            row = ' '.join(str(keyed_rows[k]))
            lines.append('{0}   {1}   {0}'.format(k, row))

        lines.append('')
        lines.append('    ' + ' '.join(str(alphabet)))

        return '\n'.join(lines)
