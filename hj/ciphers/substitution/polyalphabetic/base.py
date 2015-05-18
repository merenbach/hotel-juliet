#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import Alphabet, Transcoder, TabulaRecta


class BasePolySubCipher(SubCipher):
    """ A representation of a tabula recta cipher.

    Parameters
    ----------
    passphrase : str or string like
        An encryption/decryption key.
    tabula_recta : utils.tabula.TabulaRecta
        A tabula recta to use.
    autoclave : bool
        `True` to make this an autoclave (autokey) cipher, where
        the encrypted text will be appended to the key for decryption.

    Notes
    -----
    Autoclave only makes sense for ciphers where the passphrase is shorter than
    the message.  It might be considered a primitive form of "key stretching."

    """
    def __init__(self, passphrase, tabula_recta, autoclave):
        self.passphrase = passphrase
        self.tabula_recta = tabula_recta
        self.autoclave = autoclave
        super().__init__()


class PolySubCipher(BasePolySubCipher):
    """ A representation of a tabula recta cipher

    Parameters
    ----------
    passphrase : str or string like
        An encryption/decryption key.
    tabula_recta : utils.tabula_recta.TabulaRecta
        A tabula recta to use.
        If you cannot afford one, one will
        be provided for you at no cost to you.
    autoclave : bool, optional
        `True` to make this an autoclave (autokey) cipher, where
        the encrypted text will be appended to the key for decryption.
        Default `False`.

    """
    def __init__(self, passphrase, alphabet=None, autoclave=False):
        alphabet = Alphabet(alphabet)
        transcoders = self._make_alphabets(alphabet)
        tabula_recta = TabulaRecta(transcoders)
        super().__init__(passphrase, tabula_recta, autoclave)

    def _encode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        if strict:
            s = ''.join(c for c in s if c in self.tabula_recta.transcoders.keys())
        return self._transcode(s, reverse=False)

    def _decode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        if strict:
            s = ''.join(c for c in s if c in self.tabula_recta.transcoders.keys())
        return self._transcode(s, reverse=True)

    def _make_alphabets(self, alphabet):
        """ Create alphabets.

        """
        transcoders = {}
        for i, c in enumerate(alphabet):
            alphabet_ = alphabet.lrotate(i)
            transcoders[c] = Transcoder(alphabet, alphabet_)
        return transcoders

# def phrase(self, passphrase):
#     passphrase = list(passphrase)
#     i = iter(passphrase)
#     while True:
#         try:
#             c = next(i)
#         except StopIteration:
#             i = iter(passphrase)
#             c = next(i)
#         food = yield c
#         if food:
#             passphrase += food
#
#         yield next(n)
#         from itertools import cycle
#         x=cycle(pphrase)
#         z = yield next(x)
#         if z:
            

    def _transcode(self, s, reverse=False):
        """ Convert characters from one alphabet to another (reverse is ignored) """
        """ f is a translation function """
        passphrase = self.passphrase
        ### can add to the above
        o = []
        # Passphrase index: Number of successfully-located characters
        # Used to keep message and passphrase in "synch"
        # Character n of the message should be transcoded with character (n % passphrase len) of the passphrase
        text_autoclave = self.autoclave
        if text_autoclave and not reverse:
            passphrase += s
        # elif key_autoclave and reverse:
        #     passphrase += s
        i = 0
        for c in s:
            # if text_autoclave and c in self.tabula_recta.key_alphabet and not reverse:
            #     passphrase.append(c)
            k = passphrase[i % len(passphrase)]
            transcoded_char = self._cipher(c, k, reverse=reverse)
            # if transcoded_char in self.tabula_recta.msg_alphabet:  # [TODO] Breaks BEAUFORT
            # but above line should ideally be what we're using...
            if transcoded_char is not None and transcoded_char in self.tabula_recta.transcoders.keys():
                i += 1
                # If we are in reverse and autoclave mode, append to the passphrase
                # if text_autoclave and c in self.tabula_recta.key_alphabet and reverse:
                #     passphrase.append(transcoded_char)
                c = transcoded_char
            o.append(c)
        return ''.join(o)

    def __repr__(self):
        return repr(self.tabula_recta)
