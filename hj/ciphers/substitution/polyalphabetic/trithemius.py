#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import DEFAULT_ALPHABET


class TrithemiusCipher(VigenereCipher):
    """ Conceptual precursor to Vigenere with alphabet as countersign.

    Parameters
    ----------
    alphabet : str, optional
        A character set to use for transcoding.  Default `None`.
        If specified, will also be used as a countersign.

    Notes
    -----
    One of the least secure polyalphabetic ciphers.  This implementation
    does not allow for autoclave because it wouldn't be true to the original
    specification, where the countersign is fixed to the alphabet.

    [TODO] from a traditional standpoint, this should not have a left-hand
           column since there is no key (the key is the top row [the alphabet])

    """
    def __init__(self, alphabet=DEFAULT_ALPHABET):
        super().__init__(alphabet or DEFAULT_ALPHABET, alphabet=alphabet)
