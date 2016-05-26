#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import Cipher
import string
from utils import chunks, upward_factor, intersect
# from utils.base import grouper
# [TODO] reduce reliance on str.join method


class SubCipher(Cipher):
    """ Abstract-ish base class for substitution ciphers

    Attributes
    ----------
    DEFAULT_ALPHABET : str
        The default character set for encoding.
    DEFAULT_NULLCHAR : str
       A default string ("X") to use as padding.

    Parameters
    ----------
    alphabet : str, optional
        A plaintext alphabet to use for transcoding.  Default `None`.
    nullchar : str, optional
        A null character for padding.  Default `DEFAULT_NULLCHAR`.

    Notes
    -----
    This assumes one tableau per cipher.  If more are needed,
    refactoring may be required.

    All tableaux must have to the `.pt` and `.ct` attributes so that input and
    output character sets can be checked, for instance for chunking.  We need
    to know how many characters can be transcoded _before_ we transcode.

    """
    DEFAULT_ALPHABET = string.ascii_uppercase
    DEFAULT_NULLCHAR = 'X'

    def __init__(self, alphabet=None):
        super().__init__()
        self.tableau = self.maketableau(alphabet or self.DEFAULT_ALPHABET)

    def __repr__(self):
        return '{} ({})'.format(type(self).__name__, repr(self.tableau))

    def __str__(self):
        return str(self.tableau)

    def maketableau(self, alphabet):
        """ Create a ciphertext alphabet.

        Parameters
        ----------
        alphabet : str
            An alphabet to transform.

        Returns
        -------
        out : object
            A tableau for encryption and decryption.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError


    def encode(self, s, block=None):
        """ Encode a message.

        Parameters
        ----------
        s : str
            A message to encode.
        block : int, optional
            Divide output into blocks of this size.  All non-transcodable
            symbols will be stripped.  Specify the value `0` to strip all
            non-transcodable symbols and not divide into blocks.
            Specify the value `None` to disable chunking.  Default `None`.

        Returns
        -------
        out : str
            The encoded message.

        Notes
        -----
        Although this can invoke either `self._encode` or `super().encode`, it
        essentially falls prey to the "call super" antipattern and should
        probably be refactored. [TODO]

        """
        if block is not None:
            # filter message to characters in ciphertext alphabet
            s = ''.join(intersect(s, self.tableau.pt))

            if block > 0:
                padding = upward_factor(block, len(s))
                s = s.ljust(padding, self.DEFAULT_NULLCHAR)

        out = super().encode(s)

        if block is not None and block > 0:
            out = ' '.join(chunks(out, block))

        return ''.join(out)

    def decode(self, s, block=None):
        """ Decode a message.

        Parameters
        ----------
        s : str
            A message to decode.
        block : int, optional
            Divide output into blocks of this size.  All non-transcodable
            symbols will be stripped.  Specify the value `0` to strip all
            non-transcodable symbols and not divide into blocks.
            Specify the value `None` to disable chunking.  Default `None`.

        Returns
        -------
        out : str
            The decoded message.

        Notes
        -----
        Although this can invoke either `self._encode` or `super().encode`, it
        essentially falls prey to the "call super" antipattern and should
        probably be refactored. [TODO]

        """
        if block is not None:
            # filter message to characters in ciphertext alphabet
            s = ''.join(intersect(s, self.tableau.ct))

        out = super().decode(s)

        if block is not None and block > 0:
            padding = upward_factor(block, len(out))
            out = out.ljust(padding, self.DEFAULT_NULLCHAR)
            out = ' '.join(chunks(out, block))

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
