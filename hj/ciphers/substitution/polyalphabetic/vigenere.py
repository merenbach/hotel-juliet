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
    passphrase : str
        An encryption/decryption key.
    alphabet : str
        A character set to use for transcoding.  Default `None`.
    text_autoclave : bool, optional
        `True` to make this a text autoclave (text autokey) cipher, where
        the plaintext will be appended to the passphrase before encryption.
        Mutually exclusive with `key_autoclave`. Default `False`.
    key_autoclave : bool, optional
        `True` to make this a key autoclave (key autokey) cipher, where
        the ciphertext will be appended to the passphrase before decryption.
        Mutually exclusive with `text_autoclave`. Default `False`.

    Raises
    ------
    ValueError
        If both `text_autoclave` and `key_autoclave` are `True`.

    Notes
    -----
    Autoclave only makes sense for ciphers where the passphrase is shorter than
    the actual cipher text.

    """
    TABULA_RECTA = TabulaRecta

    def __init__(self, passphrase, alphabet=DEFAULT_ALPHABET):
        if not passphrase:
            raise ValueError('A passphrase is required')
        # try:
        #     iter(passphrase):
        # except TypeError:
        #     raise TypeError('Passphrase must be iterable')
        self.text_autoclave = False  # [TODO] remove need for this
        self.key_autoclave = False  # [TODO] remove need for this
        self.passphrase = passphrase
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
        return self._transcode(s, strict, self.passphrase, False)

    def _decode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        return self._transcode(s, strict, self.passphrase, True)

    # def _transcode_char(self, passphrase, cipher_func, strict):
    #     """ Transcode a character.
    #
    #     Parameters
    #     ----------
    #     passphrase : str
    #         A passphrase to use for transcoding.
    #     cipher_func : function
    #         A function (encode or decode) to use.
    #
    #     Yields
    #     -------
    #     out : None
    #         Waiting for message character.
    #     in : str
    #         The next message character.
    #     out : str
    #         The transcoded message character.
    #     in : str or None
    #         Character to append to keystream, or None to simply append
    #         the current keystream character.
    #
    #     """
    #     key = list(passphrase)
    #
    #     for key_char in key:
    #         msg_char = yield
    #         transcode_char = cipher_func(msg_char, key_char, strict)
    #         if transcode_char:
    #             new_kchar = yield transcode_char
    #             # append to the keystream either a new character
    #             # (in case of autoclave) or the current key character
    #             # (in the case of normal transcoding)
    #             key.append(new_kchar or key_char)
    #         # # if we instead want to provide the used key char...
    #         # msg_char = yield key_char
    #         # new_kchar = yield cipher_func(msg_char, key_char)
    #         # # append to the keystream either a new character
    #         # # (in case of autoclave) or the current key character
    #         # # (in the case of normal transcoding)
    #         # key.append(new_kchar or key_char)
    #         # ## this might or might not be more robust or performant;
    #         # ## it won't append to the key (even for default behavior
    #         # ## of cycling key) unless the current key character
    #         # ## was in the list of keys for the tableau

    def _transcode(self, message, strict, passphrase, reverse):
        """ Transcode a message.


        Parameters
        ----------
        message : str
            A message to transcode.
        reverse : bool
            `False` if we're encoding, `True` if we're decoding.

        Yields
        ------
        out : str
            The next character of the message.

        """
        _encoding_text_autoclave = self.text_autoclave and not reverse
        _decoding_text_autoclave = self.text_autoclave and reverse
        _encoding_key_autoclave = self.key_autoclave and not reverse
        _decoding_key_autoclave = self.key_autoclave and reverse

        append_input = _encoding_text_autoclave or _decoding_key_autoclave
        append_output = _encoding_key_autoclave or _decoding_text_autoclave

        cipher_func = self.tableau.decode if reverse else self.tableau.encode

        # tcoder = self._transcode_char(passphrase, cipher_func, strict)
        # prime the generator
        # tcoder.send(None)



        ####
        key = list(passphrase)  # make a mutable copy (for now)
        keystream = iter(key)

        # for key_char in key:
        #     msg_char = yield
        #     transcode_char = cipher_func(msg_char, key_char, strict)
        #     if transcode_char:
        #         new_kchar = yield transcode_char
        #         # append to the keystream either a new character
        #         # (in case of autoclave) or the current key character
        #         # (in the case of normal transcoding)
        #         key.append(new_kchar or key_char)
        ####
        key_char = None

        output = []
        for msg_char in message:
            # [NOTE] this is basically always true if `strict` is on
            # returns None if key char not found in rows
            # advance to next usable key char
            while True:
                try:
                    # use strict since we're handling non-matches ourselves
                    tchar = cipher_func(msg_char, key_char, strict=True)
                except KeyError:
                    try:
                        key_char = next(keystream)
                    except StopIteration:
                        # no valid characters within the key
                        return []
                else:
                    break

            if tchar:
                if append_output:
                    key.extend(tchar)
                elif not append_input:
                    # normal transcoding
                    # if autoclave is disabled, this has the nice side
                    # effect of causing our passphrase to loop indefinitely
                    # per the default tabula recta encryption behavior
                    key.extend(key_char)

                key_char = None
                output.extend(tchar)
            elif not strict:
                output.extend(msg_char)
        return output


class VigenereTextAutoclaveCipher(VigenereCipher):
    """ An oft-overlooked autokey cipher invented by Blaise de Vigenère.

    Notes
    -----
    In this autokey cipher, the plaintext is appended to the passphrase.
    In Vigenère's original method, a single letter was used as a "primer,"
    essentially a one-character passphrase, with the intent of encrypting
    the message with itself (minus the last message character, of course).

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_autoclave = True  # [TODO] eliminate need for this

    def _encode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        return self._transcode(s, strict, self.passphrase + s, False)


class VigenereKeyAutoclaveCipher(VigenereCipher):
    """ An oft-overlooked autokey cipher invented by Blaise de Vigenère.

    Notes
    -----
    In this autokey cipher, the ciphertext is appended to the passphrase.
    In Vigenère's original method, a single letter was used as a "primer,"
    essentially a one-character passphrase, with the intent of encrypting
    the message with itself (minus the last message character, of course).

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_autoclave = True  # [TODO] eliminate need for this

    def _decode(self, s, strict):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        return self._transcode(s, strict, self.passphrase + s, True)
