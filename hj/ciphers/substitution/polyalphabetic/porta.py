#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils.tabula_recta import DellaPortaTabulaRecta


class DellaPortaCipher(VigenereCipher):
    """ Della porta cipher.  Symmetric.

    Parameters
    ----------
    countersign : str
        An encryption/decryption key.
    alphabet : str, optional
        A plaintext alphabet.  Default `None`.

    Notes
    -----
    This is similar to the Beaufort cipher, not to be confused with the
    "variant Beaufort" cipher, which is a variant of the Vigenere.

    [TODO] ensure alphabet length is divisible by the number of items in each
    group in the leftmost (key) column

    Since this is a symmetric cipher, autoclave is not implemented.

    """
    verbose_name = 'Della Porta'

    TABULA_RECTA = DellaPortaTabulaRecta

    def __init__(self, countersign, alphabet=None):
        super().__init__(countersign, alphabet=alphabet)
