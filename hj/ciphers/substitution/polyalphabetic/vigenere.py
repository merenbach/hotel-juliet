#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import DEFAULT_ALPHABET, TabulaRecta, iterappendable

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
    ENCODE_AUTOCLAVE = lambda self, plaintext, ciphertext: None
    DECODE_AUTOCLAVE = lambda self, plaintext, ciphertext: None

    def __init__(self, countersign, alphabet=DEFAULT_ALPHABET):
        if not countersign:
            raise ValueError('A countersign is required')
        # try:
        #     iter(countersign):
        # except TypeError:
        #     raise TypeError('countersign must be iterable')
        self.countersign = countersign
        super().__init__(alphabet)
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

    def _encode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        return self._transcode(s, strict, self.tableau.encode,
                               self.ENCODE_AUTOCLAVE)

    def _decode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        return self._transcode(s, strict, self.tableau.decode,
                               self.DECODE_AUTOCLAVE)

    def _cipher_keystream(self, cipher_func, strict):
        """ Transcode a character.

        Parameters
        ----------
        countersign : str
            A countersign to use for transcoding.
        cipher_func : function
            A function (encode or decode) to use.

        Yields
        -------
        out : None
            Waiting for message character.
        in : str
            The next message character.
        out : str
            The transcoded message character.
        in : str or None
            Character to append to keystream, or None to simply append
            the current keystream character.

        """
        keystream = iterappendable(self.countersign)
        food = key_char = msg_char = None
        while True:
            # may raise StopIteration
            key_char = keystream.send(food or key_char)
            x_msg_char = None
            while x_msg_char is None:
                try:
                    x_msg_char = cipher_func(msg_char, key_char, True)
                except KeyError:
                    key_char = food = None  # invalid key char so advance
                    break
                else:
                    fallback = None if strict else msg_char
                    food = yield x_msg_char or fallback
                    msg_char = yield

    def _transcode(self, message, strict, cipher_func, keystream_extender):
        """ Transcode a message.

        Parameters
        ----------
        message : str
            A message to transcode.

        Yields
        ------
        out : data-type
            A transcoded character, if possible.  If not possible and `strict`
            is `False`, the non-transcoded character will be returned.  If not
            possible and `strict` is `True`, `None` will be returned instead.

        """
        transcoder = self._cipher_keystream(cipher_func, strict)

        _key_extension = None
        transcoder.send(None)
        for character in message:
            transcoder.send(_key_extension)  # [TODO] better?

            x_character = transcoder.send(character)
            yield x_character
            # keystream_extender = yield x_character

            _key_extension = keystream_extender(character, x_character)


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
    ENCODE_AUTOCLAVE = lambda self, plaintext, ciphertext: plaintext
    DECODE_AUTOCLAVE = lambda self, plaintext, ciphertext: ciphertext


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
    ENCODE_AUTOCLAVE = lambda self, plaintext, ciphertext: ciphertext
    DECODE_AUTOCLAVE = lambda self, plaintext, ciphertext: plaintext
