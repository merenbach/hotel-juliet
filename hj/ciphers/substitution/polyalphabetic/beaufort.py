#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import TabulaRecta, BeaufortTabulaRecta
from ciphers.substitution.monoalphabetic import AtbashCipher


class BeaufortCipher(VigenereCipher):
    """ Beaufort cipher.  Symmetric.  Not to be confused with Variant Beaufort.

    Notes
    -----
    Autoclave makes no sense for this cipher, as far as I can tell, so it is
    forced to `False`.

    Unlike the vigenere cipher, the *key* letter is located inside the grid;
    put another way, the `cipher` method in the parent class has its
    `key_char` and `msg_char` arguments swapped.  Although this implementation
    works just fine, a separate tabula recta is often described online
    to make the Vigenere cipher encode just like the Beaufort.
    [TODO] get that working and try autoclave

    To reduce code duplication, that tableau is used here.

    """
    TABULA_RECTA = BeaufortTabulaRecta

    def __init__(self, passphrase, alphabet=None):
        # alphabet = Alphabet(alphabet)
        # tableau = BeaufortTabulaRecta(alphabet)
        super().__init__(passphrase, alphabet=alphabet, autoclave=False)
        # self.tabula_recta = BeaufortTabulaRecta(alphabet, alphabet[::-1])

    # def _encode(self, s, strict):
    #     # c = AtbashCipher(self.tabula_recta.alphabet)
    #     # s = c.encode(s)
    #     o = super()._encode(s, strict)
    #     return o
    #
    # def _decode(self, s, strict):
    #     c = AtbashCipher(self.tabula_recta.alphabet)
    #     s = c.decode(s)
    #     return super()._decode(s, strict)
    #
    # def _cipher(self, msg_char, key_char, reverse):
    #     """ Convert characters from one alphabet to another
    #     (reverse is ignored) """
    #     # return self.tabula_recta.decode(key_char, msg_char)
    #     return super()._cipher(key_char, msg_char, reverse=True)
    #     # a = self.tabula_recta.alphabet
    #     # b = a[::-1]
    #     # z = str.maketrans(str(a), str(b))
    #     c = AtbashCipher(self.tabula_recta.alphabet)
    #     # if reverse:
    #     #     msg_char = c.encode(msg_char)
    #     # msg_char, key_char = key_char, msg_char
    #     # msg_char = c.encode(msg_char)
    #     # key_char = c.encode(key_char)
    #     # return super()._cipher(msg_char, key_char, reverse=True)
