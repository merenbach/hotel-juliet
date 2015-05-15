#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.alphabet import Alphabet

# def yielder(alphabet, keybet=None):
#     max_alphas = len(keybet or alphabet)
#     for n in range(max_alphas)
#         yield alphabet.lrotate(n)

from .alphabet import BaseAlphabetTranscoder
class BaseTabulaRecta(BaseAlphabetTranscoder):
    """ 

    Parameters
    ----------
    alphabet : str or string like
        An alphabet to use.
    alphabet_ : str or string like, optional
        An alternative alphabet to use for keying.

    """
    def __init__(self, alphabet, alphabet_=None):
        super().__init__(alphabet, alphabet_)

class TabulaRecta(BaseTabulaRecta):
    """ Message alphabet is on top; key alphabet is on side.

    """
    def __init__(self, msg_alphabet=None, key_alphabet=None):
        if not msg_alphabet:
            msg_alphabet = Alphabet()
        if not key_alphabet:
            key_alphabet = msg_alphabet
        self.msg_alphabet = msg_alphabet
        self.key_alphabet = key_alphabet
        super().__init__(msg_alphabet, alphabet_=key_alphabet)

    def intersect(self, col_char, row_char):
        """ Locate character within the grid.

        Parameters
        ----------
        col : str or string like
            The header character of the column to use.
        row : str or string like
            The header character of the row to use.

        Returns
        -------
        out : str
            The element at the intersection of column `col` and row `row`.

        Notes
        -----
        Order of params is not important here _except_ insofar as
        the tabula recta may not be square (e.g., Gronsfeld cipher).
        
        """
        try:
            m = self.msg_alphabet.index(str(col_char))
            k = self.key_alphabet.index(str(row_char))
        except ValueError:
            return None
        else:
            idx = (m+k) % len(self.msg_alphabet)
            out = self.msg_alphabet[idx]
            return str(out)

    def locate(self, col_char, row_char):
        """ Locate character at intersection of character `a` with row occupant character `k` """
        """ Order here *is* important, but has nothing to do with rows vs. columns """
        """ If character `a` not found, return None
        
        Returns
        -------
        out : str
            The element (encoded or plaintext) that intersects with
            edge character `msg_char` to find character `key_char`.

        """
        try:
            m = self.msg_alphabet.index(str(col_char))
            k = self.key_alphabet.index(str(row_char))
        except KeyError:
            return None
        else:
            idx = (m-k) % len(self.msg_alphabet)
            out = self.msg_alphabet[idx]
            return str(out)

    # def __repr__(self):
    #     rows = ['    ' + ' '.join(str(self.alphabet))]
    #     rows.append('  +' + '-' * 2 * len(self.alphabet))
    #     rows.extend([str(row[0]) + ' | ' + ' '.join(str(row)) for row in self.rows])
    #     return '\n'.join(rows)



    #def p(self, delimiter=' '):
    #    rows = []
    #    l = len(self.table[0].elements)
    #    rows.append(delimiter * 4 + delimiter.join(self.table[0].elements))
    #    rows.append(delimiter * 2 + '+' + '-' * (l * 2))
    #    rows.extend(row.elements[0] + ' |' + delimiter + delimiter.join(row.elements) for row in self.table)
    #    return '\n'.join(rows)
