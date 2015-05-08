#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils.tabula_recta import TabulaRecta


class PolySubCipher(SubCipher):
    """ A representation of a tabula recta cipher """
    def __init__(self, tabula_recta, passphrase, autoclave=False):
        self.passphrase = passphrase
        self.autoclave = autoclave
        if not tabula_recta:
            tabula_recta = TabulaRecta()
        self.tabula_recta = tabula_recta
        super().__init__()

    def generate_cipher_func(reverse):
        """ Default to returning the input character. Override to actually encipher/decipher anything. """
        return lambda c : c
    
    def _transcode(self, s, strict=False, reverse=False):
        """ Convert characters from one alphabet to another (reverse is ignored) """
        """ f is a translation function """
        f = self.generate_cipher_func(reverse)
        passphrase = list(self.passphrase)
        o = []
        # Passphrase index: Number of successfully-located characters
        # Used to keep message and passphrase in "synch"
        # Character n of the message should be transcoded with character (n % passphrase len) of the passphrase
        i = 0
        for c in s:
            if c in self.tabula_recta.msg_alphabet:
                if self.autoclave and c in self.tabula_recta.key_alphabet and not reverse:
                    passphrase.append(c)
                e = f(c, passphrase[i % len(passphrase)])
                if e is not None:
                    i += 1
                    o.append(e)
                    # If we are in reverse and autoclave mode, append to the passphrase
                    if self.autoclave and c in self.tabula_recta.key_alphabet and reverse:
                        passphrase.append(e)
                else:
                    # We should not get here since we're checking for alphabet membership above
                    # Situation, however, is similar to below
                    o.append(c)
            elif not strict:
                # Append the character unchanged
                # Don't update the passphrase index
                o.append(c)
        # Who is the kludgiest of them all?
        # if hasattr(s, 'join'):
        #     # Input was a string. Output will also be a string
        #     o = u''.join(o)
        return o

    def __repr__(self):
        return repr(self.tabula_recta)
