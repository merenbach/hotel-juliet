#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher

from collections import UserList


class BaseTableau(UserList):
    def __init__(self, *initlist):
        super().__init__(initlist=initlist)


class Tableau(BaseTableau):
    pass


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    plaintext_alphabet : utils.alphabet.Alphabet
        A plaintext alphabet.
    ciphertext_alphabet : utils.alphabet.Alphabet
        A ciphertext alphabet.

    """

    def __init__(self, plaintext_alphabet, ciphertext_alphabet):
        """ Initialize with source and destination character strings """
        self.alphabets = Tableau(plaintext_alphabet, ciphertext_alphabet)
        super().__init__()

    def __repr__(self):
        # [TODO] shouldn't need generator below
        return '\n'.join(repr(e) for e in self.alphabets)

    def _transcode(self, s, strict=False, reverse=False):
        """ Convert elements within a sequence to their positional counterparts in another """
        alphabets = self.alphabets
        if len(alphabets) == 2:
            if reverse:
                alphabets = alphabets[::-1]
            table = dict(zip(*alphabets))
            if not strict:
                return (table.get(c, c) for c in s)
            else:
                return (table.get(c) for c in s if table.get(c) is not None)
        return None
