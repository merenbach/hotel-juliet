#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils import Alphabet, TabulaRecta


class PolySubCipher(SubCipher):
    """ A representation of a tabula recta cipher

    Parameters
    ----------
    passphrase : str or string like
        An encryption/decryption key.
    alphabet : str or string like
        An alphabet to use for transcoding.
    key_alphabet : str or string like
        An alphabet to use to match key characters to message transcoders.
    tabula_recta : utils.tabula_recta.TabulaRecta
        A tabula recta to use.
        If you cannot afford one, one will
        be provided for you at no cost to you.
    autoclave : bool, optional
        `True` to make this an autoclave (autokey) cipher, where
        the encrypted text will be appended to the key for decryption.
        Default `False`.

    Notes
    -----
    Autoclave only makes sense for ciphers where the passphrase is shorter than

    """
    def __init__(self, passphrase, alphabet=None, autoclave=False):
        alphabet = Alphabet(alphabet)
        self.autoclave = autoclave
        self.passphrase = passphrase
        tableau = self._make_tableau(alphabet)
        super().__init__(tableau)

    def _make_tableau(self, alphabet):
        """ Create a tabula recta for transcoding.

        Parameters
        ----------
        alphabet : sequence
            An alphabet to use for transcoding.

        Returns
        -------
        out : utils.tableau.TabulaRecta
            A tabula recta to use for transcoding.

        Notes
        -----
        Since this is invoked by `__init__()` before instance is totally
        initialized, please don't perform any operations that expect a fully
        constructed instance.

        """
        return TabulaRecta(alphabet=alphabet)

    def _encode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        if strict:
            s = ''.join(c for c in s if c in self.tableau.alphabet)
        return self._transcode(s, reverse=False)

    def _decode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        if strict:
            s = ''.join(c for c in s if c in self.tableau.alphabet)
        return self._transcode(s, reverse=True)

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
            # if text_autoclave and c in self.tableau.key_alphabet and not reverse:
            #     passphrase.append(c)
            k = passphrase[i % len(passphrase)]
            # [TODO] some of this makes the assumption that a polyalphabetic
            #        cipher has a tabula recta.  Probably should be in a
            #        Vigenere subclass.
            transcoded_char = self._cipher(c, k, reverse=reverse)
            # if transcoded_char in self.tableau.msg_alphabet:  # [TODO] Breaks BEAUFORT
            # but above line should ideally be what we're using...
            if transcoded_char is not None and transcoded_char in self.tableau.alphabet:
                i += 1
                # If we are in reverse and autoclave mode, append to the passphrase
                # if text_autoclave and c in self.tableau.key_alphabet and reverse:
                #     passphrase.append(transcoded_char)
                c = transcoded_char
            o.append(c)
        return ''.join(o)
