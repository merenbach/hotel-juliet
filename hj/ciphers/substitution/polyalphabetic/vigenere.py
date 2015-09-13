#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import DEFAULT_ALPHABET, TabulaRecta, IterWrapper

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
        return self._transcoder(s, strict, self.countersign,
                                self.tableau.encode, autoclave)

    def _decode(self, s, strict, autoclave=None):
        return self._transcoder(s, strict, self.countersign,
                                self.tableau.decode, autoclave)

    def _transcoder(self, message, strict, countersign,
                    cipher_func, autoclave):
        """ Transcode a character.

        Parameters
        ----------
        message : str
            A message to transcode.
        strict : bool
            `True` to strip non-transcodeable characters, `False` otherwise.
        countersign : str
            An encryption/decryption key.
        cipher_func : function
            A function (encode or decode) to use.
        autoclave : function
            A function for autoclaving.

        Yields
        -------
        out : data-type or None
            The transcoded message character.

        """
        # msg_outer = False
        # msg_outer = True

        # both mechanisms--key outer and message outer--are the same length
        # when optimized, so far, so it's not entirely straightforward which
        # is superior, philosophically or otherwise
        # if msg_outer:
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

        # if advance_key:
        #     key_char = keystream.send(food)
        #     keystream.send('aoeu')
        #     advance_key, food = False, None
        # message = iter(message)
        # while True:
        # key_char = keystream.send(food)
        # keyset = set(countersign)
        # msgset = set(message)
        # valid_keychars = keyset & msgset

        need_next_msg = True
        need_next_key = True

        wrapped_key = IterWrapper(countersign)
        wrapped_msg = iter(message)

        while True:

            # advance semicircular message "gear"
            if need_next_msg:
                try:
                    msg_char = next(wrapped_msg)
                except StopIteration:
                    break
                else:
                    need_next_msg = False

            # advance circular key "gear"
            if need_next_key:
                try:
                    key_char = next(wrapped_key)
                except StopIteration:
                    break
                else:
                    need_next_key = False

            def transcode_it():
                try:
                    x_msg_char = next(cipher_func(msg_char, key_char))
                except StopIteration:
                    return None, True, False
                except KeyError:
                    # skip this character--not valid in key
                    return None, False, False
                else:
                    return x_msg_char, True, True

            x_msg_char, valid_keychar, valid_msgchar = transcode_it()
            if not valid_keychar:
                # skip this character--not valid in key
                need_next_key = True
            else:
                # consume next message character in next loop
                need_next_msg = True

                if valid_msgchar:
                    need_next_key = True
                    yield x_msg_char

                    # this can be here since key won't advance if transcoding
                    # was not successful
                    if autoclave:
                        add_char = autoclave(msg_char, x_msg_char)
                    else:
                        add_char = key_char
                    wrapped_key.append(add_char)

                elif not strict:
                    # key character wasn't used to transcode, but we're not
                    # in strict mode if we're here, so don't advance key
                    yield msg_char
                # else: pass

            # while True:
            #     if advance_key is True:
            #         key_char = keystream.send(food)
            #         # advance_key, food = False, None
            #         food = None

            #     try:
            #         x_msg_char = list(cipher_func(msg_char, key_char))
            #         if x_msg_char != []:
            #             x_msg_char = x_msg_char[0]
            #             could_transcode = True
            #
            #     except KeyError:
            #         # skip this character--not valid in key
            #         # advance_key = True
            #         pass
            #     else:
            #         break
            #
            # advance_key = False
            #
            # if could_transcode:
            #     out_char = x_msg_char
            #     # character was successfully transcoded
            #     if not autoclave:
            #         food = key_char
            #     else:
            #         food = autoclave(msg_char, x_msg_char)
            #     advance_key = True
            #     success = True
            #
            # elif not strict:
            #     # if not strict, x_msg_char is already set to msg_char
            #     # thanks to cipher_func
            #     out_char = msg_char
            #     success = True

            # if success:
            #     yield out_char


        # # PROS:
        # #   - no initial keystream priming
        # # CONS:
        # #   - message needs to be an iterator
        # #   - inner loop
        # #   - less clear
        # # NOTES:
        # #  - message advancement and key advancement as loops
        # message = iter(message)
        #
        # for key_char in keystream:
        #     advance_key = False
        #
        #     # this inner loop advances the message char
        #     # it avoids advancing the key until a key char is consumed
        #     while advance_key is False:
        #         msg_char = next(message)
        #         x_msg_char, success = cipher_func(msg_char, key_char, True)
        #         if success:
        #             yield x_msg_char
        #         else:
        #             yield fallback(msg_char)
        #             if not autoclave:
        #                 food = key_char
        #             else:
        #                 food = autoclave(msg_char, x_msg_char)
        #             keystream.append(food)


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
