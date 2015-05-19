#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils.base import appendable_stream


class VigenereCipher(PolySubCipher):
    """ THE Vigenere cipher, conceptual foundation of several other ciphers.

    """
    def _transcode(self, s, reverse=False):
        """ Convert characters from one alphabet to another.

        """
        passphrase = self.passphrase
        ### can add to the above
        o = []
        # Passphrase index: Number of successfully-located characters
        # Used to keep message and passphrase in "synch"
        # Character n of the message should be transcoded with character (n % passphrase len) of the passphrase
        # msg_stream = iter(s)
        # text_autoclave = self.autoclave
        # if text_autoclave and not reverse:
        #     passphrase += s
        # elif key_autoclave and reverse:
        #     passphrase += s
        # [TODO] some of this makes the assumption that a polyalphabetic
        #        cipher has a tabula recta.  Probably should be in a
        #        Vigenere subclass.
        text_autoclave = self.text_autoclave
        key_autoclave = self.key_autoclave
        # if text_autoclave and not reverse:
        #     passphrase += s
        # elif key_autoclave and reverse:
        #     passphrase += s

        keystream = appendable_stream(passphrase)
        k = keystream.send(None)  # prime the stream and get our first keychar
        for msg_char in s:
            if msg_char in self.tableau.alphabet:
                food = None
                if reverse:
                    if key_autoclave:
                        food = msg_char
                    msg_char = self.tableau.decode(msg_char, k)
                    if text_autoclave:
                        food = msg_char
                else:
                    if text_autoclave:
                        food = msg_char
                    msg_char = self.tableau.encode(msg_char, k)
                    if key_autoclave:
                        food = msg_char
                k = keystream.send(food)
            o.append(msg_char)
        return ''.join(o)
