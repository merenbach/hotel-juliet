#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import TabulaRecta
from utils.base import appendable_stream


class VigenereCipher(PolySubCipher):
    """ THE Vigenere cipher, conceptual foundation of several other ciphers.

    Parameters
    ----------
    passphrase : str
        An encryption/decryption key.
    charset : str
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

    """
    def __init__(self, passphrase, charset=None,
                 text_autoclave=False, key_autoclave=False):
        if text_autoclave and key_autoclave:
            raise ValueError('Only one of text or key autoclave may be set')
        if not passphrase:
            raise ValueError('A passphrase is required')
        # try:
        #     iter(passphrase):
        # except TypeError:
        #     raise TypeError('Passphrase must be iterable')
        self.text_autoclave = text_autoclave
        self.key_autoclave = key_autoclave
        self.passphrase = passphrase
        super().__init__(charset)

    def _make_tableau(self, charset):
        """ Create a tabula recta for transcoding.

        Parameters
        ----------
        charset : str
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
        return TabulaRecta(charset=charset)

    def _encode(self, s):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        return self._transcode(s, reverse=False)

    def _decode(self, s):
        """ [TODO] kludgy shim for now to support `reverse` arg.
        """
        return self._transcode(s, reverse=True)

    def _transcode(self, s, reverse=False):
        """ Convert characters from one alphabet to another.

        """
        ### can add to the above
        # Passphrase index: Number of successfully-located characters
        # Used to keep message and passphrase in "synch"
        # Character n of the message should be transcoded with character (n % passphrase len) of the passphrase
        # msg_stream = iter(s)
        # text_autoclave = self.autoclave
        # if text_autoclave and not reverse:
        #     passphrase += s
        # elif key_autoclave and reverse:
        #     passphrase += s
        # [TODO] some of this makes the assumption that a polyalphabetic
        #        cipher has a tabula recta.  Probably should be in a
        #        Vigenere subclass.
        # if text_autoclave and not reverse:
        #     passphrase += s
        # elif key_autoclave and reverse:
        #     passphrase += s
        encoding_text_autoclave = self.text_autoclave and not reverse
        decoding_text_autoclave = self.text_autoclave and reverse
        encoding_key_autoclave = self.key_autoclave and not reverse
        decoding_key_autoclave = self.key_autoclave and reverse

        cipher_func = self.tableau.decode if reverse else self.tableau.encode

        # def Keystream(UserString):
        #     def __init__(self, passphrase):
        #         self.passphrase = passphrase
        #
        #     def yo(self):
        #         return next(self.passphrase)
        #




#         # alternative tack:
# get usable passphrase chars: [p for p in passphrase if p in self.tableau.keys()]
# get encodeable characters: [m for m in msg if m in self.tableau.alphabet]
# for c, k in zip(encodeable_chars, usable_passphrase_chars):
#     output += 




        def gennie(s, passphrase):
            # this would include characters that don't belong
            # if encoding_text_autoclave or decoding_key_autoclave:
            #     passphrase += s

            key_elements = self.tableau.transcoders.keys() # todo make ordereddict subclass?
            passphrase = ''.join(char for char in passphrase if char in key_elements)
            # [NOTE] if passphrase is blank at this point,
            # the output will be empty.
            keystream = appendable_stream(passphrase)

            # prime the stream and get our first keychar
            for char in s:
                # [NOTE] this is basically always true if `strict` is on
                if char in self.tableau.charset:  # is this actually required?
                    ## if we don't restrict charset above...
                    # while key_char and key_char not in key_elements:
                    #     key_char = next(keystream)
                    key_char = next(keystream)
                    # advance keystream until valid char found, else break
                    # if key_char == '3': print('char = ' + char)

                    if encoding_text_autoclave or decoding_key_autoclave:
                        keystream.send(char)

                    # returns None if key char not found in rows
                    char = cipher_func(char, key_char)

                    if encoding_key_autoclave or decoding_text_autoclave:
                        keystream.send(char)

                yield char
            # msg = iter(s)
            # for kchar in keystream:
            #     char = next(msg)
            #     if char in self.tableau.charset:
            #

            # prime the stream and get our first keychar
            # mchariter = iter(s)
            # for kchar in keystream:
            #     # [NOTE] this is basically always true if `strict` is on
            #     while:
            #         char = next(mchariter)
            #         if char in self.tableau.alphabet:
            #             char = cipher_func(char, kchar)
            #
            #             if encoding_key_autoclave or decoding_text_autoclave:
            #                 keystream.send(char)
            #         yield char

        # consume iter(s) up to a point, then continue, etc.

        # msg_iter = iter(s)
        # key_iter = iter(passphrase)
        # msg_len = len(s)
        # key_len = len(passphrase)
        #
        # full_msg_out = []
        # msg_encoded = []
        # while:
        #     full_msg_out.extend(msg_encoded)
        #     key_iter = iter(msg_encoded)
        #     for key_char in key_iter:
        #         msg_char = next(msg_iter):
        #         try:
        #             msg_encoded.append(None)  # encode
        #         except StopIteration:
        #             # we ran out of key characters
        #             break
        #     if msg exhausted:
        #         break
        #
        # output = []
        # segment = []
        # key_iter = iter(passphrase)
        # for msg_char in msg_iter:
        #     char = msg_char
        #     if can_transcode(msg_char):  # should just return None in tabula?
        #         try:
        #             msg_char = encode(msg_char, next(key_iter))
        #             segment.append(msg_char)
        #         except StopIteration:
        #             if post_autoclave:
        #                 key_iter = iter(segment[:])
        #             else:
        #                 key_iter = iter(passphrase)
        #             segment.clear()
        #     output.append(char)
        #


        o = [n for n in gennie(s, self.passphrase)]
        # current_stretch = o
        # if encoding_key_autoclave or decoding_text_autoclave:
        #     for i in range(20):
        #         g = gennie(s[len(o):], current_stretch)
        #         current_stretch = (n for n in g)
        #         o.extend(current_stretch)
        return ''.join(o)
