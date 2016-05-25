#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import extendable_iterator, TabulaRecta

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
    def __init__(self, countersign, alphabet=None):
        super().__init__()

        self.tableau = self.maketableau(alphabet or self.DEFAULT_ALPHABET)

        self.countersign = [e for e in countersign if e in self.tableau.key_alphabet]
        if not self.countersign:
            raise ValueError('A countersign is required')

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

    def _transcoder(self, message, cipher_func, autoclave_func):
        keystream = extendable_iterator(self.countersign)
        key_char = next(keystream)
        # key_char = yield

        # iterate over (finite!) message in outer loop with standard "for"
        for msg_char in message:
            try:
                x_msg_char = cipher_func(msg_char, key_char)

            except ValueError:
                # message char not transcodeable
                # strict must be off, or this character wouldn't still be here
                # yield the raw character
                yield msg_char

            else:
                yield x_msg_char
                key_food = autoclave_func(msg_char, x_msg_char)

                # this can be here since key won't advance if transcoding
                # was not successful
                key_char = keystream.send(key_food or key_char)

    def _encode_autoclave(self, msg_char, x_msg_char): return None
    def _decode_autoclave(self, msg_char, x_msg_char): return None

    def _encode(self, s):
        return self._transcoder(s, self.tableau.encipher, self._encode_autoclave)

    def _decode(self, s):
        return self._transcoder(s, self.tableau.decipher, self._decode_autoclave)


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
    def _encode_autoclave(self, msg_char, x_msg_char): return msg_char
    def _decode_autoclave(self, msg_char, x_msg_char): return x_msg_char


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
    def _encode_autoclave(self, msg_char, x_msg_char): return x_msg_char
    def _decode_autoclave(self, msg_char, x_msg_char): return msg_char
