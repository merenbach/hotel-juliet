#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import Alphabet
from utils import TabulaRecta


class VigenereCipher(PolySubCipher):
    """ THE Vigenère cipher, conceptual foundation of several other ciphers.

    Despite its name, it was not created by Blaise de Vigenère, who instead
    created an autokey cipher.

    Parameters
    ----------
    countersign : str
        An encryption/decryption key.
    alphabet : str
        A plaintext alphabet.  Default `None`.

    """
    @staticmethod
    def _autoclave_encode(before, after): return None

    @staticmethod
    def _autoclave_decode(before, after): return None

    def __init__(self, countersign, alphabet=None):
        super().__init__()
        alphabet = Alphabet(alphabet)
        self.tableau = self.maketableau(alphabet)
        self.countersign = countersign

    @staticmethod
    def maketableau(alphabet):
        """ Create a tabula recta for transcoding.

        Parameters
        ----------
        alphabet : str
            A character set to use for transcoding.

        Returns
        -------
        out : utils.tableau.TabulaRecta
            A tabula recta to use for transcoding.

        """
        return TabulaRecta(alphabet)

    def _encode(self, s):
        cs = list(c for c in self.countersign if c in self.tableau.keys)
        if not cs:
            return

        keystream = iter(cs)
        key_char = next(keystream)
        for c in s:
            try:
                x_msg_char = self.tableau.pt2ct(c, key_char)
            except ValueError:
                yield c
            else:
                yield x_msg_char

                key_food = self._autoclave_encode(c, x_msg_char)
                cs.extend(key_food or key_char)
                key_char = next(keystream)

    def _decode(self, s):
        cs = list(c for c in self.countersign if c in self.tableau.keys)
        if not cs:
            return

        keystream = iter(cs)
        key_char = next(keystream)
        for c in s:
            try:
                x_msg_char = self.tableau.ct2pt(c, key_char)
            except ValueError:
                yield c
            else:
                yield x_msg_char

                key_food = self._autoclave_decode(c, x_msg_char)
                cs.extend(key_food or key_char)
                key_char = next(keystream)


class VigenereTextAutoclaveCipher(VigenereCipher):
    """ An oft-overlooked autokey cipher developed by Blaise de Vigenère.

    Notes
    -----
    In this autokey cipher, the plaintext is appended to the countersign.
    In Vigenère's original method, a single letter was used as a "primer,"
    essentially a one-character countersign, with the intent of encrypting
    the message with (almost all) of itself.  It becomes much more effective
    when the key length is more than a single character.

    The autokey mechanism offers no additional security (in fact, it has no
    effect at all) unless the key is shorter than the text to be encrypted.

    """
    ENCODE_AUTOCLAVE = 0

    @staticmethod
    def _autoclave_encode(before, after): return before

    @staticmethod
    def _autoclave_decode(before, after): return after


class VigenereKeyAutoclaveCipher(VigenereCipher):
    """ An oft-overlooked autokey cipher developed by Blaise de Vigenère.

    Notes
    -----
    In this autokey cipher, the ciphertext is appended to the countersign.
    In Vigenère's original method, a single letter was used as a "primer,"
    essentially a one-character countersign, with the intent of encrypting
    the message with (almost all) of itself.  It becomes much more effective
    when the key length is more than a single character.

    The autokey mechanism offers no additional security (in fact, it has no
    effect at all) unless the key is shorter than the text to be encrypted.

    """
    ENCODE_AUTOCLAVE = 1

    @staticmethod
    def _autoclave_encode(before, after): return after

    @staticmethod
    def _autoclave_decode(before, after): return before
