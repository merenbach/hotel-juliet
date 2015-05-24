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

    def _transcode_char(self, passphrase, cipher_func):
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
        key = list(passphrase)

        for key_char in key:
            msg_char = yield
            transcode_char = cipher_func(msg_char, key_char)
            if transcode_char:
                new_kchar = yield transcode_char
                # append to the keystream either a new character
                # (in case of autoclave) or the current key character
                # (in the case of normal transcoding)
                key.append(new_kchar or key_char)
            # # if we instead want to provide the used key char...
            # msg_char = yield key_char
            # new_kchar = yield cipher_func(msg_char, key_char)
            # # append to the keystream either a new character
            # # (in case of autoclave) or the current key character
            # # (in the case of normal transcoding)
            # key.append(new_kchar or key_char)
            # ## this might or might not be more robust or performant;
            # ## it won't append to the key (even for default behavior
            # ## of cycling key) unless the current key character
            # ## was in the list of keys for the tableau

    def _transcode_message(self, message, reverse):
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

        # [TODO] make ordereddict subclass?
        key_elements = self.tableau.transcoders
        passphrase = [char for char in self.passphrase if char in key_elements]

        tcoder = self._transcode_char(passphrase, cipher_func)
        # prime the generator
        tcoder.send(None)

        for msg_char in message:
            # [NOTE] this is basically always true if `strict` is on
            if msg_char in self.tableau.charset:  # is this actually required?
                # returns None if key char not found in rows
                tchar = tcoder.send(msg_char)

                if append_input:
                    autokey_append = msg_char
                elif append_output:
                    autokey_append = tchar
                else:
                    # normal transcoding
                    # if autoclave is disabled, this has the nice side
                    # effect of causing our passphrase to loop indefinitely
                    # per the default tabula recta encryption behavior
                    autokey_append = None

                tcoder.send(autokey_append)
                msg_char = tchar
            yield msg_char

    def _transcode(self, s, reverse=False):
        """ Convert characters from one alphabet to another.

        """
        # Passphrase index: Number of successfully-located characters
        # Used to keep message and passphrase in "synch"
        # Character n of the message should be transcoded with character
        # (n % passphrase len) of the passphrase

        return ''.join(self._transcode_message(s, reverse))
        #         # alternative tack:
        # get usable passphrase chars: [p for p in passphrase
        #                               if p in self.tableau.keys()]
        # get encodeable characters: [m for m in msg
        #                             if m in self.tableau.alphabet]
        # [H, E, L, L, O, ',', ' ', W, O, R, L, D]
        # [O, C, E, A, N, nil, nil, O, C, E, A, N]
        # kchars = [n for n in cycle passphrase if tcodeable msg
        #           at same pos...]
        # for c, k in zip(encodeable_chars, usable_passphrase_chars):
        #     output += ...

        # this would include characters that don't belong
        # if append_input:
        #     passphrase += s
        # [NOTE] if passphrase is blank at this point,
        # the output will be empty.
        # prime the stream and get our first keychar

        # ## feeding msg to transcoder containing key...
        # ## would other way around be better? feed next key to msg tcoder?
