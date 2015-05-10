#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from collections import UserString, OrderedDict
from .base import lrotated, keyed


class BaseAlphabet(UserString):
    """ Base alphabet class with only unique elements in initlist.

    """
    # def __init__(self, seq):
    #     super().__init__(seq)

    def __lshift__(self, by):
        """ Shift a copy of this alphabet to the left with the << operator.

        Parameters
        ----------
        by : int
            Shift by this many elements.

        Returns
        -------
        out : type(self)
            A left-shifted copy of this alphabet.

        """
        return lrotated(self, by)

    def __rshift__(self, by):
        """ Shift a copy of this alphabet to the right with the >> operator.

        Parameters
        ----------
        by : int
            Shift by this many elements.

        Returns
        -------
        out : type(self)
            A right-shifted copy of this alphabet.

        """
        return lrotated(self, -by)

    def reversed(self):
        """ Reverse a copy of this alphabet.

        Returns
        -------
        out : type(self)
            A reversed copy of this alphabet.

        """
        seq = self.data[::-1]
        return type(self)(seq)

# class BaseAlphabet(UserList):
#     """ Base alphabet class with only unique elements in initlist.

#     Raises
#     ------
#     TypeError
#         If `initlist` is not iterable.

#     Notes
#     -----
#     The goal of this class is to make alternative alphabets, such as with
#     tuples instead of letters, a viable option if some unlikely situation
#     requires.  Also good for integers!

#     """
#     def __init__(self, initlist=None):
#         if initlist:
#             # [TODO] convert to list first?
#             initlist = OrderedDict.fromkeys(initlist)
#         super().__init__(initlist=initlist)

#     def __lshift__(self, by):
#         """ Shift to the left with the << operator.

#         Parameters
#         ----------
#         by : int
#             Shift by this many elements.

#         Returns
#         -------
#         out : type(self)
#             A left-shifted copy of this alphabet.

#         """
#         return lrotated(self, by)

#     def __rshift__(self, by):
#         """ Shift to the right with the >> operator.

#         Parameters
#         ----------
#         by : int
#             Shift by this many elements.

#         Returns
#         -------
#         out : type(self)
#             A right-shifted copy of this alphabet.

#         """
#         return lrotated(self, -by)

#     def reversed(self):
#         """ Reverse a copy of this list.

#         Returns
#         -------
#         out : type(self)
#             A reversed copy of this list.

#         """
#         initlist = reversed(self)
#         return type(self)(initlist)


class Alphabet(BaseAlphabet):
    """ A string-based alphabet.

    Attributes
    ----------
    DEFAULT_ALPHABET : str
        A Unicode string of characters to use when none are specified.
        Alphabets may make use of non-string sequences for their members.

    Notes
    -----
    We convert to strings first.
    Technically any hashable item (e.g., tuple) should work,
    but it is difficult to test for every eventuality, and
    there are optimizations (str.maketrans/str.translate)
    that will remain unavailable if strings aren't assumed
    *somewhere*:

        initlist = [str(n) for n in initlist]  # example

    Totally string-agnostic items get refactored into BaseAlphabet.

    """
    DEFAULT_ALPHABET = string.ascii_uppercase

    """ Represent a string of unique characters """
    def __init__(self, seq=None):
        # If no alphabet is specified, use a "default" of ASCII uppercase
        if not seq:
            seq = self.DEFAULT_ALPHABET
        else:
            seq = ''.join(OrderedDict.fromkeys(str(seq)))
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

    def find(self, c):
        """ Return the index of a given element.

        Parameters
        ----------
        c : data-type
            An element for which to retrieve an index.

        Returns
        -------
        int : the index of the provided element, or `-1` if not found.
        """
        try:
            return self.data.index(c)
        except ValueError:
            return -1

    def keyed(self, key):
        """ Key a copy of this alphabet.

        Parameters
        ----------
        seq : sequence
            A sequence with which to key this alphabet.

        Returns
        -------
        out : type(self)
            A keyed copy of this alphabet.

        Notes
        -----
        Only elements already in this list may be prepended.
        Duplicates will be removed.

        This should work on non-string types, but hasn't been tested
        extensively with them.

        """
        return keyed(self, key)

    def affinal(self, m, b, inverse=False):
        return Alphabet(self._affinal(m, b, inverse=inverse))

    def _affinal(self, m, b, inverse=False):
        def xgcd(a, b):
            """ Extended Euclidean algorithm to find divisors and solve Bezout's identity
                Returns (x, y, gcd(a, b)) such that ax + by = gcd(a, b)
            """
            print("**** ALPHABET._AFFINAL.XGCD DEPRECATED BY FRACTION.GCD LIBRARY FUNCTION")
            if b == 0:
                return (1, 0, a)
            else:
                (x, y, d) = xgcd(b, a % b)
                return (y, x - (a // b) * y, d)

        def affine_transform(elements, m, b, inverse=False):
            """ m = multiplier, b = additive (a la y = mx + b)"""
            char_len = len(elements)
            if char_len > 0:
                gcd = xgcd(char_len, m)
                # Ensure lack of coprimality: result of "1" indicates *not* coprime
                if gcd[2] == 1:
                    if not inverse:
                        position = lambda x : (m * x + b) % char_len
                    else:
                        # Get the modular multiplicative inverse
                        mmi = (gcd[1] + char_len) % char_len
                        position = lambda x : (mmi * (x - b + char_len)) % char_len
                    return ''.join([elements[position(x)] for x in range(char_len)])
            return ''

        return affine_transform(self.data, m, b, inverse=inverse)

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

# Subclasses for each cipher?  Then rotate/key/etc. in init()...

# class AtbashAlphabet(Alphabet):
#     def __init__(self, initlist, shift):
#         initlist.shift(3)
#         super().__init__(initlist=initlist)

# a =AtbashAlphabet

# c = Cipher(a, b)
# null char should be a "None" instead of an actual character?
