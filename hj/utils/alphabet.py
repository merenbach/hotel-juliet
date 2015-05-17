#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from collections import UserString
from .base import at_modulo, lrotated, multiplied, unique
# import itertools


##
## [TODO]: Better way to manipulate alphabets when creating cipher objects...
## maybe only do in encode/decode methods?
## todo: grouping/null chars
## todo: running keys/autokeys (text and cipher)

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
        # [TODO] reexamine: `if not seq` => blank alphabets
        # become full ones, so lrotated(alpha, 0) gives weird
        # results
        # If no alphabet is specified, use a "default" of ASCII uppercase
        if seq is None:
            seq = self.DEFAULT_ALPHABET

        seq = ''.join(unique(str(seq)))
        super().__init__(seq)

    def at(self, pos):
        """ Return the element at a given index, wrapping as needed.

        Parameters
        ----------
        pos : int
            An integer index to retrieve.  Will be wrapped if out of bounds.

        Returns
        -------
        out : data-type
            The element at the given index, or `None` if `self` has length 0.

        """
        seq = at_modulo(self, pos)
        return self._recast(seq)

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

    def common(self, s):
        """ Return a supplied string stripped of characters not in this alphabet """
        print('**** ALPHABET.COMMON WILL BE DEPRECATED')
        f = lambda c: c in self.data
        return filter(f, s)

    # def __repr__(self):
    #     return repr(''.join((str(e) for e in self)))
