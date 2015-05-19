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
    def __init__(self, passphrase, alphabet=None,
                 text_autoclave=False, key_autoclave=False):
        if text_autoclave and key_autoclave:
            raise ValueError('Only one of text or key autoclave may be set')
        alphabet = Alphabet(alphabet)
        self.text_autoclave = text_autoclave
        self.key_autoclave = key_autoclave
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
        raise NotImplementedError
