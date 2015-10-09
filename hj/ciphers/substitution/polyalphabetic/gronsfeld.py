#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import DEFAULT_ALPHABET
from utils.tabula_recta import GronsfeldTabulaRecta


class GronsfeldCipher(VigenereCipher):
    """ Vigenere with only ten key alphabets, corresponding to 0..9.

    Parameters
    ----------
    countersign : str
        An encryption/decryption key.
    alphabet : str, optional
        A character set to use for transcoding.  Default `None`.

    Notes
    -----
    Since the countersign is numeric, autoclave makes less sense here.
    Technically, it can be made totally symmetric if a Beaufort tabula recta
    is used instead.

    """
    TABULA_RECTA = GronsfeldTabulaRecta

    def __init__(self, countersign, alphabet=DEFAULT_ALPHABET):
        super().__init__(countersign, alphabet=alphabet)
