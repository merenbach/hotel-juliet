#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import PortaTabulaRecta


class PortaCipher(PolySubCipher):
    """ Della porta cipher.  Symmetric.

    Notes
    -----
    This is a variant of the Beaufort cipher, not to be confused with the
    "variant Beaufort" cipher, which is a variant of the Vigenere.

    [TODO] ensure alphabet length is divisible by the number of items in each
    group in the leftmost (key) column
    [TODO] does/should this support autoclave?

    """
    TABULA_RECTA = PortaTabulaRecta
    # def __init__(self, passphrase, alphabet=None, autoclave=False):
    #     tableau = PortaTabulaRecta(alphabet)
    #     super().__init__(passphrase, tableau=tableau, autoclave=autoclave)

    def _cipher(self, msg_char, key_char, reverse=False):
        """ Convert characters from one alphabet to another
        (reverse is ignored) """
        # return super()._cipher(msg_char, key_char, reverse=reverse)
        return self.tabula_recta.decode(msg_char, key_char)
