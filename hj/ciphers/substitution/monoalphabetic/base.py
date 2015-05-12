#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils.alphabet import Alphabet


class BaseMonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str or string like
        A source (plaintext) alphabet to underlie transcoding.
    alphabet_ : str or string like
        A destination (ciphertext) alphabet to underlie transcoding.

    Raises
    ------
    ValueError
        If `alphabet` and `alphabet_` have unequal length.

    """
    def __init__(self, alphabet, alphabet_):
        """ Initialize with source and destination character strings """
        if len(alphabet) != len(alphabet_):
            raise ValueError('Alphabets must have equal length')
        self.alphabet, self.alphabet_ = alphabet, alphabet_
        super().__init__()

    def __repr__(self):
        return '{}\n{}'.format(self.alphabet, self.alphabet_)


class MonoSubCipher(BaseMonoSubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str or string like
        A source (plaintext) alphabet to underlie transcoding.
    operations : iterable
        An iterable of operations to perform on the initial alphabet.

    Notes
    -----
    The `BaseMonoSubCipher` class may be initialized with only strings.
    This class assumes existence of the Alphabet utility class, so for
    philosophical reasons it is separated out here.

    Raises
    ------
    ValueError
        If `alphabet` and `alphabet_` have unequal length.

    """
    def __init__(self, alphabet, operations):
        alphabet = Alphabet(alphabet)
        alphabet_ = alphabet.translate(operations)
        super().__init__(alphabet, alphabet_)

    def encode(self, *args, **kwargs):
        """ Encode a message.  All params passed through to `_transcode()`.

        Returns
        -------
        out : sequence
            A encoded message.

        """
        table = self._translation_table(reverse=False)
        return self._transcode(table, *args, **kwargs)

    def decode(self, *args, **kwargs):
        """ Decode a message.  All params passed through to `_transcode()`.

        Returns
        -------
        out : sequence
            A decoded message.

        """
        table = self._translation_table(reverse=True)
        return self._transcode(table, *args, **kwargs)

    def _translation_table(self, reverse=False):
        """ Create a string translation table.

        Parameters
        ----------
        reverse : bool, optional
            `True` to reverse the conversion direction, `False` otherwise.
            Defaults to `False`.

        Returns
        -------
        out : dict
            A translation between alphabets.

        """
        alphabets = str(self.alphabet), str(self.alphabet_)
        if reverse:
            alphabets = reversed(alphabets)
        return str.maketrans(*alphabets)

    def _transcode(self, translation_table, s, strict=False):
        """ Convert elements within a sequence.

        Parameters
        ----------
        translation_table : dict
            A dict mapping ordinal source characters to destination characters.
        s : sequence
            A sequence to encode.
        strict : bool, optional
            `True` to strip all characters not in this cipher's alphabet,
            `False` to funnel through to output.  Defaults to `False`.

        Returns
        -------
        out : sequence
            A transcoded message.

        """
        if strict:
            from utils.base import testscreened
            s = testscreened(s, self.alphabet)
        return s.translate(translation_table)
