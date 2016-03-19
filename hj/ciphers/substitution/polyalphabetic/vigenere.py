#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import extendable_iterator, TabulaRecta

# [TODO] still need to add keyed alphabets per Vigenere


class BaseVigenereCipher(PolySubCipher):
    """ Base class for THE Vigenere cipher.

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
        if not alphabet:
            alphabet = self.DEFAULT_ALPHABET
        self.tableau = self._make_tableau(alphabet)
        self.countersign = [e for e in countersign if e in self.tableau.key_table]
        if not self.countersign:
            raise ValueError('A countersign is required')

    def _make_tableau(self, alphabet):
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
        # [TODO] the tabula recta could perhaps handle?
        return self._transcoder(s, self.tableau.encode)

    def _decode(self, s):
        # [TODO] the tabula recta could perhaps handle?
        return self._transcoder(s, self.tableau.decode)

    def _transcoder(self, message, cipher_func):
        """ Transcode a character.

        Parameters
        ----------
        message : str
            A message to transcode.
        cipher_func : function
            A function (encode or decode) to use.

        Yields
        -------
        out : data-type or None
            The transcoded message character.

        """
        wrapped_key = extendable_iterator(self.countersign)
        key_char = wrapped_key.send(None)

        # iterate over (finite!) message in outer loop with standard "for"
        for msg_char in message:
            try:
                x_msg_char_out = cipher_func(msg_char, key_char)

            except ValueError:
                # message char not transcodeable
                # strict must be off, or this character wouldn't still be here
                # yield the raw character
                yield msg_char, None

            else:
                key_food = yield x_msg_char_out, msg_char

                # this can be here since key won't advance if transcoding
                # was not successful
                key_char = wrapped_key.send(key_food or key_char)


class VigenereCipher(BaseVigenereCipher):
    """ THE Vigenère cipher, conceptual foundation of several other ciphers.

    Despite its name, it was not created by Blaise de Vigenère, who instead
    created an autokey cipher.

    Parameters
    ----------
    countersign : str
        An encryption/decryption key.
    alphabet : str
        A character set to use for transcoding.  Default `None`.

    """
    def _encode(self, s):
        for e_after, __ in super()._encode(s):
            yield e_after
        # generator = super()._encode(s)
        # while True:
        #     try:
        #         e_after, __ = next(generator)
        #     except StopIteration:
        #         return
        #     else:
        #         yield e_after

    def _decode(self, s):
        for e_after, __ in super()._decode(s):
            yield e_after
        # generator = super()._decode(s)
        # while True:
        #     try:
        #         e_after, __ = next(generator)
        #     except StopIteration:
        #         return
        #     else:
        #         yield e_after

class VigenereTextAutoclaveCipher(BaseVigenereCipher):
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
    def _encode(self, s):
        generator = super()._encode(s)
        try:
            food = None
            while True:
                e_after, e_before = generator.send(food)
                food = [e_before]
                yield e_after
        except StopIteration:
            return

    def _decode(self, s):
        generator = super()._decode(s)
        try:
            food = None
            while True:
                e_after, __ = generator.send(food)
                food = [e_after]
                yield e_after
        except StopIteration:
            return


class VigenereKeyAutoclaveCipher(BaseVigenereCipher):
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
    def _encode(self, s):
        generator = super()._encode(s)
        try:
            food = None
            while True:
                e_after, __ = generator.send(food)
                food = [e_after]
                yield e_after
        except StopIteration:
            return

    def _decode(self, s):
        generator = super()._decode(s)
        try:
            food = None
            while True:
                e_after, e_before = generator.send(food)
                food = [e_before]
                yield e_after
        except StopIteration:
            return
