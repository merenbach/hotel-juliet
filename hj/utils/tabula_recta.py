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
        super().__init__(alphabet, alphabet_ or alphabet)


class TabulaRecta(BaseTabulaRecta):
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    alphabet : str or string like, optional
        An alphabet to use.  Message encoding will occur with this alphabet.
        The message and this alphabet must have overlapping character sets.
    alphabet_ : str or string like, optional
        A cipher alphabet to use.  Passphrase keying will occur with this
        alphabet.  The passphrase and this alphabet must have overlapping
        character sets.

    Notes
    -----
    Since (en/de)ciphering is done positionally with math, it really doesn't
    matter whether the two alphabets are the same length or even whether
    they have any of the same characters.

    As long as the passphrase (in the polyalphabetic cipher) and the alphabet
    passed in have the same character set (or rather, provided that the
    key alphabet is a superset of the passphrase character set), everything
    will translate fine.  Random Unicode glyphs could be used.

    """
    def __init__(self, alphabet=None, alphabet_=None):
        super().__init__(alphabet, alphabet_)
        # [TODO] kludgy vars that shouldn't be here
        self.msg_alphabet = self.alphabet
        self.key_alphabet = self.alphabet_

    def _find(self, m, k, func):
        """ Locate character within the grid.

        Parameters
        ----------
        m : str
            The header character of the message alphabet to use.
        k : str
            The header character of the key alphabet to use.

        Returns
        -------
        out : str
            The element at the location determined by `func`.

        """
        try:
            i = self.alphabet.index(m)
            j = self.alphabet_.index(k)
        except ValueError:
            return None
        else:
            pos = func(i, j)
            element = self.alphabet.at(pos)
            return str(element)

    def intersect(self, m, k):
        """ Locate character within the grid.

        Parameters
        ----------
        m : str
            The header character of the message alphabet to use.
        k : str
            The header character of the key alphabet to use.

        Returns
        -------
        out : str
            The element at the intersection of column `col` and row `row`.

        Notes
        -----
        Order of params is not important here _except_ insofar as
        the tabula recta may not be square (e.g., Gronsfeld cipher).

        """
        f = lambda a, b: a + b
        return self._find(m, k, f)

    def locate(self, col_char, k):
        """ Locate character at intersection of character `a`
        with row occupant character `k`.

        Parameters
        ----------
        col : str
            The header character of the column to use.
        k : str
            The header character of the key alphabet row to use.

        Returns
        -------
        out : str
            The element (encoded or plaintext) that intersects with
            edge character `msg_char` to find character `key_char`.
            If no match found, return `None`.

        Notes
        -----
        Order here *is* important, but has nothing to do with rows vs. columns

        """
        f = lambda a, b: a - b
        return self._find(col_char, k, f)

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
