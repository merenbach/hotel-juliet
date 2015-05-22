#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from collections import UserString
from .base import default_charset, unique
# import itertools


##
## [TODO]: Better way to manipulate alphabets when creating cipher objects...
## maybe only do in encode/decode methods?
## todo: grouping/null chars
## todo: running keys/autokeys (text and cipher)

# class BaseAlphabet(UserString):
#     """ Base alphabet class.
#
#     Notes
#     -----
#     The goal of this class is to make alternative alphabets, such as with
#     tuples instead of letters, a viable option at some point in the future
#     if some unlikely situation requires.  Also maybe integers!
#
#     A behavioral goal to achieve the above would be to be able to substitute
#     in a UserList as the superclass here instead of a UserString.  Clearly
#     that poses issues with the extensive use of `str.maketrans()` and
#     `str.translate()` for most of the encoding throughout the program.
#
#     Because of that, this is considered a low philosophical priority.
#
#     """
#     def _recast(self, seq):
#         """ Recast a sequence as type of self.
#
#         Parameters
#         ----------
#         seq : sequence
#             Recast this as `type(self)`.
#
#         Returns
#         -------
#         out : type(self)
#             A copy of `seq` cast to `type(self)`.
#
#         """
#         return type(self)(seq)
#
#     def lrotate(self, by):
#         """ Shift a copy of this sequence to the left.
#
#         Parameters
#         ----------
#         by : int
#             Shift by this many elements.
#
#         Returns
#         -------
#         out : type(self)
#             A left-shifted copy of this sequence.
#
#         """
#         seq = lrotated(self, by)
#         return self._recast(seq)
#
#     def reverse(self):
#         """ Reverse a copy of this sequence.
#
#         Returns
#         -------
#         out : type(self)
#             A reversed copy of this sequence.
#
#         """
#         seq = reversed(self)
#         return self._recast(seq)
#
#     def __lshift__(self, by):
#         """ Shorthand for left rotation with <<.
#
#         """
#         return self.lrotate(by)
#
#     def __rshift__(self, by):
#         """ Shorthand for right rotation with >>.
#
#         """
#         return self.lrotate(-by)
#
#     def __invert__(self):
#         """ Shorthand for reversal with ~.
#
#         """
#         return self.reverse()


class Alphabet(UserString):
    """ A string-based alphabet.


    """
    def __init__(self, seq=None):
        # [TODO] reexamine: `if not seq` => blank alphabets
        # become full ones, so lrotated(alpha, 0) gives weird
        # results
        # If no alphabet is specified, use a "default" of ASCII uppercase

        seq = ''.join(unique(str(seq or default_charset)))
        super().__init__(seq)

    # def reverse(self):
    #     """ Reverse a copy of this sequence.
    #
    #     Returns
    #     -------
    #     out : type(self)
    #         A reversed copy of this sequence.
    #
    #     """
    #     seq = reversed(self)
    #     return self._recast(seq)
    #
    # def _recast(self, seq):
    #     """ Recast a sequence as type of self.
    #
    #     Parameters
    #     ----------
    #     seq : sequence
    #         Recast this as `type(self)`.
    #
    #     Returns
    #     -------
    #     out : type(self)
    #         A copy of `seq` cast to `type(self)`.
    #
    #     Notes
    #     -----
    #     [TODO] Add mechanism to flatten sequence of strings. (??)
    #
    #     """
    #     if isinstance(self, (str, UserString)):
    #         seq = ''.join(str(s) for s in seq)
    #     return type(self)(seq)
