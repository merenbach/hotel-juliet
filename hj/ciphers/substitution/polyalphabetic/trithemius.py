#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import Alphabet


class TrithemiusCipher(VigenereCipher):
    """ Conceptual precursor to Vigenere.

    Parameters
    ----------
    passphrase : str
        An encryption/decryption key.
    charset : str, optional
        A character set to use for transcoding.  Default `None`.

    Notes
    -----
    Not especially secure as passphrase is simply the alphabet.
    Autoclave isn't a feature of this cipher mainly because it wouldn't be true
    to the original (insecure) design.

    """
    def __init__(self, charset=None):
        alphabet = Alphabet(charset)
        super().__init__(alphabet, charset=alphabet)
