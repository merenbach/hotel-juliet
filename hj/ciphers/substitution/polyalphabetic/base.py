#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils.tabula_recta import TabulaRecta


class BasePolySubCipher(SubCipher):
    """ A representation of a tabula recta cipher.

    Parameters
    ----------
    passphrase : str or string like
        An encryption/decryption key.
    tabula_recta : utils.tabula_recta.TabulaRecta
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
        tabula_recta = TabulaRecta(alphabet)
        super().__init__(passphrase, tabula_recta, autoclave)

    def _encode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        if strict:
            s = self.tabula_recta.sanitize(s)
        return self._transcode(s, strict, False)

    def _decode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        if strict:
            s = self.tabula_recta.sanitize(s)
        return self._transcode(s, strict, True)

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
            

    def _transcode(self, s, strict=False, reverse=False):
        """ Convert characters from one alphabet to another (reverse is ignored) """
        """ f is a translation function """
        passphrase = self.passphrase
        ### can add to the above
        o = []
        # Passphrase index: Number of successfully-located characters
        # Used to keep message and passphrase in "synch"
        # Character n of the message should be transcoded with character (n % passphrase len) of the passphrase
        i = 0
        for c in s:
            if c in self.tabula_recta.msg_alphabet:
                if self.autoclave and c in self.tabula_recta.key_alphabet and not reverse:
                    passphrase.append(c)
                e = self._cipher(c, str(passphrase[i % len(passphrase)]),
                        reverse=reverse)
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
        return ''.join(o)

    def __repr__(self):
        return repr(self.tabula_recta)
