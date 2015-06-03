#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import Cipher
from utils import unique, DEFAULT_ALPHABET
# from utils.base import grouper
# [TODO] still need to implement grouping/blocks


class SubCipher(Cipher):
    """ Abstract-ish base class for substitution ciphers

    Attributes
    ----------
    DEFAULT_NULLCHAR : str
       A default string ("X") to use as padding.

    Parameters
    ----------
    alphabet : str
        A character set to use for transcoding.
    nullchar : str, optional
        A null character for padding.  Default `DEFAULT_NULLCHAR`.

    Notes
    -----
    This assumes one tableau per cipher.  If more are needed,
    refactoring may be required.

    """
    DEFAULT_NULLCHAR = 'X'

    def __init__(self, alphabet, nullchar=DEFAULT_NULLCHAR):
        super().__init__()
        alphabet = unique(alphabet or DEFAULT_ALPHABET)
        self.nullchar = nullchar

    def _make_tableau(self, alphabet):
        """ Create a tableau for transcoding.

        Parameters
        ----------
        alphabet : sequence
            A character set to use for transcoding.

        Returns
        -------
        out : data-type
            A tableau to use for transcoding.

        Raises
        ------
        NotImplementedError
            If not overridden.

        Notes
        -----
        Since this is invoked by `__init__()` before instance is totally
        initialized, please don't perform any operations that expect a fully
        constructed instance.

        """
        raise NotImplementedError

    def __repr__(self):
        # [TODO] maybe improve this
        return repr(self.tableau)

    def __str__(self):
        # [TODO] maybe improve this
        return str(self.tableau)

    def encode(self, s, strict=False, block=0):
        """ Encode a message.

        Parameters
        ----------
        s : str
            A message to encode.
        strict : bool, optional
            `True` to strip non-transcodeable characters from the string,
            `False` otherwise.
        block : int, optional
            NOT YET IMPLEMENTED.  Divide output into blocks of this size.

        Returns
        -------
        out : str
            The encoded message.

        """
        out = self._encode(s, strict=strict)
        return ''.join(out)

    def decode(self, s, strict=False, block=0):
        """ Decode a message.

        Parameters
        ----------
        s : str
            A message to decode.
        strict : bool, optional
            `True` to strip non-transcodeable characters from the string,
            `False` otherwise.
        block : int, optional
            NOT YET IMPLEMENTED.  Divide output into blocks of this size.

        Returns
        -------
        out : str
            The decoded message.

        """
        out = self._decode(s, strict=strict)
        return ''.join(out)

    # def unblockify(self, iterable, n, fillvalue=None):
    #     """ From itertools"""
    #     iterable = iterable.replace(self.separator, '')
    #     groups = grouper(iterable, n, fillvalue=self.nullchar)
    #     print(list(groups))
    #     # out = [''.join(g) for g in groups]
    #     return ''.join(iterable)
    #
    # def blockify(self, iterable, n, fillvalue=None):
    #     """ From itertools"""
    #     groups = grouper(iterable, n, fillvalue=self.nullchar)
    #     # print(list(groups))
    #     out = [''.join(g) for g in groups]
    #     return ' '.join(out)


    # def transcode(self, s, strict=False, block=0, reverse=False):
    #     """ Transcode an input sequence. This may be called directly with the same default effect as `encode`.
    #     
    #     Parameters
    #     ----------
    #     s       : sequence
    #               A string, list, tuple, or other sequence to transcode.
    #     strict  : boolean, optional, default `False`
    #               `True` to strip from the message any elements not in the message alphabet,
    #               `False` otherwise.
    #     block   : integer, optional, default `0`
    #               If greater than zero, this will divide up the transcoded sequence into groups of `block` elements apiece.
    #               This has no effect if `strict` is `False`.
    #     reverse : boolean, optional, default `False`
    #               `True` if this is a reverse (i.e., decryption) operation, `False` otherwise.
    #     
    #     Returns
    #     -------
    #     list : the transcoded sequence, converted (if not already a list) to list form.
    #     """
    #     return self._transcode(s, strict=strict, reverse=reverse)
    #
    #     if not self.use_strings:
    #         # Special preprocessing for non-string sequences
    #         from itertools import chain
    #         # KLUDGE to flatten a possibly nested sequence
    #         try:
    #             seq = chain.from_iterable(s)
    #         except TypeError:
    #             seq = s
    #     else:
    #         seq = s
    #     if strict and block > 0:
    #         # Add a set of nulls (the same number as the block size) to the end
    #         seq.extend(self.nullchar * block)
    #     t = self._transcode(seq, strict=strict, reverse=reverse)
    #     if strict and block > 0:
    #         # This requires some explaining:
    #         # Because of our null character padding (above), a group of elements was added to the input
    #         # prior to encoding. Let's say strict mode is True, block size is 5, null padding char is 'X'.
    #         # Our input has XXXXX at the end, regardless of length.  Once the output is generated, that
    #         # input *still* has the equivalent of the five nulls at the end, but they're encoded.  If
    #         # the last group has five characters, then the message divided evenly into the block size and no nulls
    #         # were needed.  If four, three, two, or one character are shown, then one or more nulls was added to the
    #         # previous group and the last group has the "remainder" (very much analogous to modular arithmetic).
    #         # Rather than do anything especially clever, we can *no matter what* drop the last group without hesitation:
    #         # regardless of its *size*, it is all null characters and we don't need it anymore to make things align
    #         # properly with the block size!
    #         #import itertools
    #         #s = u' '.join(list(itertools.izip_longest(*(iter(s),) * block, fillvalue=None)))
    #         t = [tuple(t[i:i+block]) for i in range(0, len(t), block)][:-1]
    #         if self.use_strings:
    #             # Special postprocessing for strings
    #             t = (u''.join(e) for e in t)
    #             return u' '.join(t)
    #     elif self.use_strings:
    #         return u''.join(t)
    #     else:
    #         return t
    #     
    # def _transcode(self, s, strict=False, reverse=False):
    #     """ Do nothing, really, save for return the message """
    #     return s
