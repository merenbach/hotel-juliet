#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import DEFAULT_ALPHABET, TabulaRecta

# [TODO] still need to add keyed alphabets per Vigenere


class VigenereCipher(PolySubCipher):
    """ THE Vigenere cipher, conceptual foundation of several other ciphers.

    Despite its name, it was not created by Blaise de Vigenère, who instead
    created an autokey cipher.

    Parameters
    ----------
    countersign : str
        An encryption/decryption key.
    alphabet : str
        A character set to use for transcoding.  Default `None`.

    """
    TABULA_RECTA = TabulaRecta

    def __init__(self, countersign, alphabet=DEFAULT_ALPHABET):
        if not countersign:
            raise ValueError('A countersign is required')
        # try:
        #     iter(countersign):
        # except TypeError:
        #     raise TypeError('countersign must be iterable')
        super().__init__(alphabet)
        self.countersign = countersign
        self.tableau = self._make_tableau(alphabet or DEFAULT_ALPHABET)

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
        return self.TABULA_RECTA(alphabet=alphabet)

    def _encode(self, s, strict, autoclave=None):
        return self._transcoder(s, strict, self.tableau.encode, autoclave)

    def _decode(self, s, strict, autoclave=None):
        return self._transcoder(s, strict, self.tableau.decode, autoclave)

    def _transcode_char(self, msg_char, key_char, strict, cipher_func):
        """ Transcode a single character.

        """
        x_msg_char = cipher_func(msg_char, key_char, True)
        success = x_msg_char is not None

        if strict:
            msg_char = None  # no fallback
        return x_msg_char or msg_char, success

    def _transcoder(self, message, strict, cipher_func, autoclave):
        """ Transcode a character.

        Parameters
        ----------
        countersign : str
            A countersign to use for transcoding.
        cipher_func : function
            A function (encode or decode) to use.

        Yields
        -------
        out : data-type or None
            The transcoded message character.

        """
        keystream = self.tableau.keystream_from(self.countersign)

        # msg_outer = False
        msg_outer = True

        # both mechanisms--key outer and message outer--are the same length
        # when optimized, so far, so it's not entirely straightforward which
        # is superior, philosophically or otherwise
        if msg_outer:
            # PROS of this mechanism:
            #   - no inner loop
            #   - iterate over the message outside (more imp. philosophically
            #     than the passphrase)
            #   - fairly straightforward logic
            #   - message needn't be an iterator
            # CONS:
            #   - `advance` bool required
            # NOTES:
            #   - key advancement in conditional, not loop

            advance_key, food = True, None
            for msg_char in message:
                if advance_key is True:
                    key_char = keystream.send(food)

                x_msg_char, advance_key = self._transcode_char(msg_char, key_char, strict, cipher_func)
                yield x_msg_char

                if advance_key is True and autoclave is not None:
                    food = autoclave(msg_char, x_msg_char)
                else:
                    food = key_char

        else:
            # PROS:
            #   - no initial keystream priming
            # CONS:
            #   - message needs to be an iterator
            #   - inner loop
            #   - less clear
            # NOTES:
            #  - message advancement and key advancement as loops
            message = iter(message)

            for key_char in keystream:
                advance_key = False

                # this inner loop advances the message char
                # it avoids advancing the key until a key char is consumed
                while advance_key is False:
                    msg_char = next(message)
                    x_msg_char, advance_key = process_char(msg_char, key_char)
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
    def _encode(self, s, strict):
        autoclave = lambda plaintext, ciphertext: plaintext
        return super()._encode(s, strict, autoclave=autoclave)

    def _decode(self, s, strict):
        autoclave = lambda plaintext, ciphertext: ciphertext
        return super()._decode(s, strict, autoclave=autoclave)


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
    def _encode(self, s, strict):
        autoclave = lambda plaintext, ciphertext: ciphertext
        return super()._encode(s, strict, autoclave=autoclave)

    def _decode(self, s, strict):
        autoclave = lambda plaintext, ciphertext: plaintext
        return super()._decode(s, strict, autoclave=autoclave)
