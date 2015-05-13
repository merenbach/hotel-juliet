#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from collections import UserString
from .base import lrotated, multiplied, unique
# import itertools


class BaseAlphabet(UserString):
    """ Base alphabet class.

    Notes
    -----
    The goal of this class is to make alternative alphabets, such as with
    tuples instead of letters, a viable option at some point in the future
    if some unlikely situation requires.  Also maybe integers!

    """
    def _recast(self, seq):
        """ Recast a sequence as type of self.

        Parameters
        ----------
        seq : sequence
            Recast this as `type(self)`.

        Returns
        -------
        out : type(self)
            A copy of `seq` cast to `type(self)`.

        Notes
        -----
        [TODO] Add mechanism to flatten sequence of strings. (??)

        """
        if isinstance(self, (str, UserString)):
            seq = ''.join(str(s) for s in seq)
        return type(self)(seq)

    def reverse(self):
        """ Shift a copy of this sequence to the left.

        Parameters
        ----------
        by : int
            Shift by this many elements.

        Returns
        -------
        out : type(self)
            A left-shifted copy of this sequence.

        """
        seq = reversed(self)
        return self._recast(seq)

    def lrotate(self, by):
        """ Shift a copy of this sequence to the left with the << operator.

        Parameters
        ----------
        by : int
            Shift by this many elements.

        Returns
        -------
        out : type(self)
            A left-shifted copy of this sequence.

        """
        seq = lrotated(self, by)
        return self._recast(seq)

    def __invert__(self):
        """ Shorthand for reversing an alphabet with ~.

        """
        return self.reverse()

    def __lshift__(self, by):
        """ Shorthand for left rotation with <<.

        """
        return self.lrotate(by)

    def __rshift__(self, by):
        """ Shorthand for right rotation with >>.

        """
        return self.lrotate(-by)



class Alphabet(BaseAlphabet, UserString):
    """ A string-based alphabet.

    Attributes
    ----------
    DEFAULT_ALPHABET : str
        A Unicode string of characters to use when none are specified.

    """
    DEFAULT_ALPHABET = string.ascii_uppercase

    """ Represent a string of unique characters """
    def __init__(self, seq=None):
        # If no alphabet is specified, use a "default" of ASCII uppercase
        if not seq:
            seq = self.DEFAULT_ALPHABET

        seq = ''.join(unique(str(seq)))
        super().__init__(seq)

    def element(self, i):
        """ Return the element at a given index.

        Parameters
        ----------
        i : int
            An integer index to try to retrieve. Returns None on out-of-bounds.

        Returns
        -------
        data-type : the element at the provided index, or `None` if not found.
        """
        print('**** ALPHABET.COMMON WILL BE DEPRECATED')
        try:
            return self.data[i]
        except IndexError:
            return None

    def keyed(self, seq):
        """ Key a copy of the given sequence.

        Parameters
        ----------
        seq : sequence
            A sequence with which to key a copy of self.

        Returns
        -------
        out : type(self)
            A copy of `self` keyed with `seq`.

        Notes
        -----
        Only elements already in self will be used for keying.

        """
        # [TODO] make this much, much better
        # filter elements not in `self` from `seq`
        seq = [element for element in seq if element in self]
        seq += [element for element in self if element not in seq]
        return self._recast(seq)

    def multiply(self, by):
        """ Multiply the position of each character in self.

        Notes
        -----
        Rename this.

        """
        seq = multiplied(self, by)
        return self._recast(seq)

    # def __getitem__(self, i):
    #     """ Return the proper type when doing a slice.

    #     http://stackoverflow.com/questions/27552379/why-a-userlist-subclass-appears-to-return-the-wrong-type-for-slicing

    # Note: the problem here is that the init() method checks if the arg is a UserList and, if so, it changes it to a
    #       regular list via [:] prior to storing it in the data ivar.  If "copying" through a slice returns a UserList,
    #       something might break.
    #     """
    #     res = super().__getitem__(i)
    #     if isinstance(i, slice):
    #         res = type(self)(res)
    #     return res

    # def __str__(self):
    #     return ''.join(self)

    def translate(self, operations):
        """ Run a sequence of operations on a copy of this alphabet.

        Parameters
        ----------
        operations : iterable
            A sequence of operations to perform.

        Returns
        -------
        out : type(self)
            A character translation dict.

        """
        translation = self
        if operations:
            for op in operations:
                translation = op.handle(translation)
        return type(self)(translation)

    def common(self, s):
        """ Return a supplied string stripped of characters not in this alphabet """
        print('**** ALPHABET.COMMON WILL BE DEPRECATED')
        f = lambda c: c in self.data
        return filter(f, s)

    # def __repr__(self):
    #     return repr(''.join((str(e) for e in self)))

# class AtbashAlphabet(Alphabet):
#     def __init__(self, initlist, shift):
#         initlist.shift(3)
#         super().__init__(initlist=initlist)

# a =AtbashAlphabet

# c = Cipher(a, b)
# null char should be a "None" instead of an actual character?


# class BaseMessage(UserString):
#     """ Represent a string-based message to transcode.

#     """
#     def __init__(self, seq, alphabet=None):
#         self.alphabet = Alphabet(alphabet)
#         super().__init__(seq)


# class Message(BaseMessage):
#     """ Represent a string-based message to transcode.

#     """
#     def encoded(self, cipher):
#         """ Encode a message.  All params passed through to `_transcode()`.

#         Returns
#         -------
#         out : sequence
#             A encoded message.

#         """
#         for arg in args:
#             arg.encode()
#         table = self._translation_table(reverse=False)
#         return self._transcode(table, *args, **kwargs)

#     def decoded(self, cipher):
#         """ Decode a message.  All params passed through to `_transcode()`.

#         Returns
#         -------
#         out : sequence
#             A decoded message.

#         """
#         table = self._translation_table(reverse=True)
#         return self._transcode(table, *args, **kwargs)

#     def _translation_table(self, reverse=False):
#         """ Create a string translation table.

#         Parameters
#         ----------
#         reverse : bool, optional
#             `True` to reverse the conversion direction, `False` otherwise.
#             Defaults to `False`.

#         Returns
#         -------
#         out : dict
#             A translation between alphabets.

#         """
#         # null = ''
#         # if strict:
#         #     null = ''.join(set(s) - set(self.alphabet))
#         # return str.maketrans(a1, a2, null)

#         alphabets = str(self.alphabet), str(self.alphabet_)
#         if reverse:
#             alphabets = reversed(alphabets)
#         return str.maketrans(*alphabets)

#     def _transcode(self, translation_table, s, strict=False):
#         """ Convert elements within a sequence.

#         Parameters
#         ----------
#         translation_table : dict
#             A dict mapping ordinal source characters to destination characters.
#         s : sequence
#             A sequence to encode.
#         strict : bool, optional
#             `True` to strip all characters not in this cipher's alphabet,
#             `False` to funnel through to output.  Defaults to `False`.

#         Returns
#         -------
#         out : sequence
#             A transcoded message.

#         """
#         if strict:
#             from utils.base import testscreened
#             s = testscreened(s, self.alphabet)
#         return s.translate(translation_table)
