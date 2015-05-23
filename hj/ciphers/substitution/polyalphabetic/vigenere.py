#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import PolySubCipher
from utils import TabulaRecta


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

        def transcode_char(passphrase):
            """ Transcode a character.

            Parameters
            ----------
            msg_char : str
                A message character to transcode.
            passphrase : str
                A passphrase to use for transcoding.

            Yields
            -------
            out : str
                The transcoded message character.

            """
            key = list(passphrase)

            for key_char in iter(key):
                msg_char = yield
                # # if we instead want to provide the used key char...
                # msg_char = yield key_char
                transcode_char = cipher_func(msg_char, key_char)
                if transcode_char:
                    new_kchar = yield transcode_char
                    # append to the keystream either a new character
                    # (in case of autoclave) or the current key character
                    # (in the case of normal transcoding)
                    key.append(new_kchar or key_char)




#         # alternative tack:
# get usable passphrase chars: [p for p in passphrase if p in self.tableau.keys()]
# get encodeable characters: [m for m in msg if m in self.tableau.alphabet]
# [H, E, L, L, O, ',', ' ', W, O, R, L, D]
# [O, C, E, A, N, nil, nil, O, C, E, A, N]
# kchars = [n for n in cycle passphrase if tcodeable msg at same pos...]
# for c, k in zip(encodeable_chars, usable_passphrase_chars):
#     output += 

        def tcode(s, passphrase):
            # this would include characters that don't belong
            # if encoding_text_autoclave or decoding_key_autoclave:
            #     passphrase += s
            key_elements = self.tableau.transcoders.keys() # todo make ordereddict subclass?
            passphrase = [char for char in passphrase if char in key_elements]
            # [NOTE] if passphrase is blank at this point,
            # the output will be empty.
            # prime the stream and get our first keychar

            ### feeding msg to transcoder containing key...
            ### would other way around be better? feed next key to msg tcoder?
            tcoder = transcode_char(passphrase)
            key_char = tcoder.send(None)
            for char in s:
                # [NOTE] this is basically always true if `strict` is on
                if char in self.tableau.charset:  # is this actually required?
                    # returns None if key char not found in rows
                    tchar = tcoder.send(char)

                    if encoding_text_autoclave or decoding_key_autoclave:
                        autokey_append = char
                    elif encoding_key_autoclave or decoding_text_autoclave:
                        autokey_append = tchar
                    else:
                        # normal transcoding
                        # if autoclave is disabled, this has the nice side
                        # effect of causing our passphrase to loop indefinitely
                        # per the default tabula recta encryption behavior
                        autokey_append = None

                    tcoder.send(autokey_append)
                    char = tchar

                yield char

        o = [n for n in tcode(s, self.passphrase) if n is not None]
        return ''.join(o)
