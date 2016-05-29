#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import intersect, TabulaRecta
import itertools

# [TODO] still need to add keyed alphabets per Vigenere


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
        self.tableau = self.maketableau(alphabet or self.DEFAULT_ALPHABET)
        self.countersign = intersect(countersign, self.tableau.rows)
        if not self.countersign:
            raise ValueError('A countersign is required.')

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

        Notes
        -----
        Since this is invoked by `__init__()` before instance is totally
        initialized, please don't perform any operations that expect a fully
        constructed instance.

        """
        return TabulaRecta(alphabet)

    def _encode(self, s):
        countersign = list(self.countersign)

        keystream = itertools.cycle(countersign)
        key_char = next(keystream)
        for c in s:
            row = self.tableau.rows.get(key_char)
            if row and c in row.pt:
                x_msg_char = c.translate(row.pt2ct)
                key_food = self._autoclave_encode(c, x_msg_char)
                countersign.extend(key_food or [])
                key_char = next(keystream)
            else:
                x_msg_char = c
            yield x_msg_char

    def _decode(self, s):
        countersign = list(self.countersign)

        keystream = itertools.cycle(countersign)
        key_char = next(keystream)
        for c in s:
            row = self.tableau.rows.get(key_char)
            if row and c in row.ct:
                x_msg_char = c.translate(row.ct2pt)
                key_food = self._autoclave_decode(c, x_msg_char)
                countersign.extend(key_food or [])
                key_char = next(keystream)
            else:
                x_msg_char = c
            yield x_msg_char


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
