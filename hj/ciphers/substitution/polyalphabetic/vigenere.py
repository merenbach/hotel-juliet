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

    """
    TABULA_RECTA = TabulaRecta

    def __init__(self, passphrase, alphabet=DEFAULT_ALPHABET):
        if not passphrase:
            raise ValueError('A passphrase is required')
        # try:
        #     iter(passphrase):
        # except TypeError:
        #     raise TypeError('Passphrase must be iterable')
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

    def _cipher_keystream(self, cipher_func):
        """ Transcode a character.

        Parameters
        ----------
        passphrase : str
            A passphrase to use for transcoding.
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
        key = list(self.passphrase)
        character = yield
        for key_char in key:
            try:
                transcode_char = cipher_func(character, key_char, True)
            except KeyError:
                pass
            else:
                if transcode_char:  # character was transcodable!
                    new_kchar = yield transcode_char
                    # append to the keystream either a new character
                    # (in case of autoclave) or the current key character
                    # (in the case of normal transcoding)
                    key.extend(new_kchar or key_char)  # [TODO] should be append
                    character = yield
    #         # # if we instead want to provide the used key char...
    #         # character = yield key_char
    #         # new_kchar = yield cipher_func(character, key_char)
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

        Returns
        -------
        out : list
            The transcoded text.

        """
        output = []

        cipher_func = self.tableau.decode if reverse else self.tableau.encode

        # tcoder = self._transcode_char(passphrase, cipher_func, strict)
        # prime the generator
        # tcoder.send(None)


        keystream = self._cipher_keystream(cipher_func)

        next(keystream)  # prime the keystream
        try:
            for character in message:
                # [NOTE] this is basically always true if `strict` is on
                # returns None if key char not found in rows
                # advance to next usable key char
                if self.tableau.contains(character):  # [TODO] if character in self.tableau
                    tchar = keystream.send(character)
                    if tchar:
                        _key_extension = self._extend_keystream(character,
                                                                tchar,
                                                                reverse)
                        keystream.send(_key_extension)  # [TODO] better?
                        character = tchar
                    # elif not strict:
                    #     output.extend(character)
                elif strict:
                    character = None

                if character:
                    output.extend(character)

        except StopIteration:
            pass
        return output

    def _extend_keystream(self, plaintext, ciphertext, reverse):
        return None


class VigenereTextAutoclaveCipher(VigenereCipher):
    """ An oft-overlooked autokey cipher invented by Blaise de Vigenère.

    Notes
    -----
    In this autokey cipher, the plaintext is appended to the passphrase.
    In Vigenère's original method, a single letter was used as a "primer,"
    essentially a one-character passphrase, with the intent of encrypting
    the message with itself (minus the last message character, of course).

    The autokey mechanism offers no additional security (in fact, it has no
    effect at all) unless the key is shorter than the text to be encrypted.

    """
    def _extend_keystream(self, plaintext, ciphertext, reverse):
        return reverse and ciphertext or plaintext


class VigenereKeyAutoclaveCipher(VigenereCipher):
    """ An oft-overlooked autokey cipher invented by Blaise de Vigenère.

    Notes
    -----
    In this autokey cipher, the ciphertext is appended to the passphrase.
    In Vigenère's original method, a single letter was used as a "primer,"
    essentially a one-character passphrase, with the intent of encrypting
    the message with itself (minus the last message character, of course).

    The autokey mechanism offers no additional security (in fact, it has no
    effect at all) unless the key is shorter than the text to be encrypted.

    """
    def _extend_keystream(self, plaintext, ciphertext, reverse):
        return reverse and plaintext or ciphertext
