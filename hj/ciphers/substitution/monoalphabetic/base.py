#!/usr/bin/python
# -*- coding: utf-8 -*-

from ciphers.substitution import *

class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder """
    
    def __init__(self, plaintext_alphabet, ciphertext_alphabet):
        """ Initialize with source and destination character strings """
        self.alphabets = (plaintext_alphabet, ciphertext_alphabet)
        super(MonoSubCipher, self).__init__()
    
    def __repr__(self):
        return u'\n'.join(repr(e) for e in self.alphabets)
    
    def _transcode(self, s, strict=False, reverse=False):
        """ Convert elements within a sequence to their positional counterparts in another """
        if len(self.alphabets) == 2:
            if reverse:
                alphabets = (alphabet.elements for alphabet in self.alphabets[::-1])
            else:
                alphabets = (alphabet.elements for alphabet in self.alphabets)
            table = dict(zip(*alphabets))
            if not strict:
                return (table.get(c, c) for c in s)
            else:
                return (table.get(c) for c in s if table.get(c) is not None)
        return None
