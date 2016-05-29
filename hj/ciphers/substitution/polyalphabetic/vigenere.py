#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import extendable_iterator, intersect, TabulaRecta

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
    ENCODE_AUTOCLAVE = None
    DECODE_AUTOCLAVE = None

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
        keystream = extendable_iterator(self.countersign)
        key_char = next(keystream)
        for c in s:
            row = self.tableau.rows.get(key_char)
            if row and c in row.pt:
                x_msg_char = c.translate(row.pt2ct)
                key_food = (None, c, x_msg_char)[self.ENCODE_AUTOCLAVE or 0]
                key_char = keystream.send(key_food or key_char)
            else:
                x_msg_char = c
            yield x_msg_char

    def _decode(self, s):
        keystream = extendable_iterator(self.countersign)
        key_char = next(keystream)
        for c in s:
            row = self.tableau.rows.get(key_char)
            if row and c in row.ct:
                x_msg_char = c.translate(row.ct2pt)
                key_food = (None, c, x_msg_char)[self.DECODE_AUTOCLAVE or 0]
                key_char = keystream.send(key_food or key_char)
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
    ENCODE_AUTOCLAVE = 1
    DECODE_AUTOCLAVE = 2

    # def _encode(self, s):
    #     return self._transcoder(s, self.tableau.encipher, ARGS_FIRST)

    # def _decode(self, s):
    #     return self._transcoder(s, self.tableau.decipher, ARGS_LAST)


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
    ENCODE_AUTOCLAVE = 2
    DECODE_AUTOCLAVE = 1

    # def _encode(self, s):
    #     return self._transcoder(s, self.tableau.encipher, ARGS_LAST)

    # def _decode(self, s):
    #     return self._transcoder(s, self.tableau.decipher, ARGS_FIRST)
