#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.alphabet import Alphabet

# def yielder(alphabet, keybet=None):
#     max_alphas = len(keybet or alphabet)
#     for n in range(max_alphas)
#         yield alphabet.lrotate(n)

class BaseTabulaRecta:
    def __init__(self, alphabet, keybet=None):
        self.alphabet = alphabet
        max_alphas = len(keybet or alphabet)
        rows = [alphabet.lrotate(n) for n in range(max_alphas)]
        # self.rows = rows

        # alphabet_list = list(yielder(alphabet, keybet))
        self.alphabets = dict(zip(keybet or alphabet, rows))
        # if not keybet:
        #     self.alphabets = {alphabet[0]: alphabet for alphabet in alphabets}
        # else:
        #     keybetiter = iter(keybet)
        #     abetiter = iter(alphabets)
        #     # self.alphabets = {next(keybetiter): alphabet for alphabet in alphabets}
        #     self.alphabets = {k: next(abetiter) for k in keybet}

    def intersect(self, col, row, coerce=False):
        if coerce:
            try:
                col = self.col_headers.index(col)
                row = self.row_headers.index(row)
            except ValueError:
                raise
            else:
                return self.intersect(col, row, coerce=False)
        return self.alphabets[row][col]

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
        super().__init__(msg_alphabet, keybet=key_alphabet)

    def intersect(self, msg_char, key_char):
        """ Locate character at intersection of characters `a` and `b` """
        try:
            row, col = self.alphabets[key_char], self.alphabet.index(msg_char)
        except (KeyError, IndexError):
            return None
        else:
            out = row[col]
            return str(out)

    def locate(self, msg_char, key_char):
        """ Locate character at intersection of character `a` with row occupant character `k` """
        """ Order here *is* important, but has nothing to do with rows vs. columns """
        """ If character `a` not found, return None """
        try:
            row = self.alphabets[key_char]
        except KeyError:
            return None
        else:
            idx = row.index(msg_char)
            out = self.alphabet[idx]
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
