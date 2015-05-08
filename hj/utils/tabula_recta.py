#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.alphabet import Alphabet


class TabulaRecta:
    def __init__(self, msg_alphabet=None, key_alphabet=None):
        if not msg_alphabet:
            msg_alphabet = Alphabet()
        if not key_alphabet:
            key_alphabet = msg_alphabet
        self.msg_alphabet = msg_alphabet
        self.key_alphabet = key_alphabet
        row_keys = tuple(k for k in key_alphabet)
        self.keyed_table = dict((row_keys[i], msg_alphabet << i) for i in range(len(key_alphabet)))
        self.index_table = tuple(msg_alphabet << i for i in range(len(key_alphabet)))

    def key_row(self, k):
        """ Return a full (possibly-wrapped) alphabet from a given row, denoted by initial char `key_char` """
        return self.keyed_table.get(k, None)

    # def idx_row(self, k):
    #     idx = self.key_alphabet.find(k)
    #     if idx != -1:
    #         return self.index_table[idx]
    #     return None

    def intersect(self, msg_char, key_char):
        """ Locate character at intersection of characters `a` and `b` """
        r = self.key_row(key_char)
        if r is not None:
            idx = self.msg_alphabet.find(msg_char)
            if idx != -1:
                return r.element(idx)
        return None

    def locate(self, msg_char, key_char):
        """ Locate character at intersection of character `a` with row occupant character `k` """
        """ Order here *is* important, but has nothing to do with rows vs. columns """
        """ If character `a` not found, return None """
        r = self.key_row(key_char)
        if r is not None:
            idx = r.find(msg_char)
            if idx != -1:
                return self.msg_alphabet.element(idx)
        return None

    #def p(self, delimiter=' '):
    #    rows = []
    #    l = len(self.table[0].elements)
    #    rows.append(delimiter * 4 + delimiter.join(self.table[0].elements))
    #    rows.append(delimiter * 2 + '+' + '-' * (l * 2))
    #    rows.extend(row.elements[0] + ' |' + delimiter + delimiter.join(row.elements) for row in self.table)
    #    return '\n'.join(rows)
