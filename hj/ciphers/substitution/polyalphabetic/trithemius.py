#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .vigenere import VigenereCipher
from utils import default_charset


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

    [TODO] is there a way to make this even simpler w/r/t mechanism?

    """
    def __init__(self, charset=None):
        super().__init__(charset or default_charset, charset=charset)
