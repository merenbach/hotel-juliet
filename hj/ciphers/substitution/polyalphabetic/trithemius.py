#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import DEFAULT_ALPHABET


class TrithemiusCipher(VigenereCipher):
    """ Conceptual precursor to Vigenere with alphabet as passphrase.

    Parameters
    ----------
    alphabet : str, optional
        A character set to use for transcoding.  Default `None`.
        If specified, will also be used as a passphrase.

    Notes
    -----
    One of the least secure polyalphabetic ciphers.  This implementation
    does not allow for autoclave because it wouldn't be true to the original
    specification, where the passphrase is fixed to the alphabet.

    """
    def __init__(self, alphabet=DEFAULT_ALPHABET):
        super().__init__(alphabet or DEFAULT_ALPHABET, alphabet=alphabet)
