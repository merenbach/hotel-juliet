# -*- coding: utf-8 -*-

import string
from .base import rotated, flipped
from collections import UserList


class Alphabet(UserList):
    """
    Attributes
    ----------
    DEFAULT_ALPHABET : str
                       A Unicode string of characters to use when none are specified.
                       Alphabets may make use of non-string sequences for their members.

    Parameters
    ----------
    initlist : sequence
        A sequence.

    uniqueify
    nullchar
    """
    DEFAULT_ALPHABET = string.ascii_uppercase
    
    """ Represent a string of unique characters """
    def __init__(self, initlist=None, uniqueify=True, nullchar=None):
        if not initlist:
            # If no alphabet is specified, use a "default" of ASCII uppercase
            initlist = self.DEFAULT_ALPHABET
        # Ensure that characters are unique
        if uniqueify:
            # Render the characters within the alphabet unique prior to storing them
            initlist = [c for i, c in enumerate(initlist) if not c in initlist[:i]]
        super().__init__(initlist=initlist)
    
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

    def contains(self, c):
        """ Test whether this alphabet contains an element.
        
        Parameters
        ----------
        c : data-type
            An element for which to try to determine membership.
        
        Returns
        -------
        boolean : `true` if this alphabet contains the element, `false` otherwise.
        """
        if self.find(c) == -1:
            return False
        else:
            return True

    def affinal(self, m, b, inverse=False):
        return Alphabet(self._affinal(m, b, inverse=inverse), uniqueify=False)
    
    def _affinal(self, m, b, inverse=False):
        def xgcd(a, b):
            """ Extended Euclidean algorithm to find divisors and solve Bezout's identity
                Returns (x, y, gcd(a, b)) such that ax + by = gcd(a, b)
            """
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
                    return u''.join([elements[position(x)] for x in range(char_len)])
            return u''
        
        return affine_transform(self.data, m, b, inverse=inverse)

    # def __getitem__(self, i):
    #     """ Return the proper type when doing a slice.

    #     http://stackoverflow.com/questions/27552379/why-a-userlist-subclass-appears-to-return-the-wrong-type-for-slicing

    #     """
    #     res = super().__getitem__(i)
    #     if isinstance(i, slice):
    #         res = type(self)(res)
    #     return res

    def flipped(self):
        """ Return a reversed version of this alphabet.

        """
        transformed = flipped(self)
        return Alphabet(transformed, uniqueify=False)

    def keyed(self, keyword):
        """ Return a "codeword" version of this alphabet """
        return Alphabet(self._keyed(keyword=keyword), uniqueify=True)

    def _keyed(self, keyword):
        """ Return a "codeword" version of this alphabet as a string """
        # Restrict keyword to characters already in the alphabet
        # This helps to prevent inadvertent "extension" of the alphabet
        # This is more efficient but uniquifying throws an error
        #return Uniqueifier().uniqueify([c for c in keyword if c in self.data] + self.data)
        return self.common(list(keyword)) + self.data

    def _wrapped(self, offset):
        """ Return a wrapped copy (left shifted) of this alphabet as a string """
        return rotated(self, offset)

    def common(self, s):
        """ Return a supplied string stripped of characters not in this alphabet """
        f = lambda c: c in self.data
        return filter(f, s)

    #def shifted(self, by):
    #    """ Method to left-shift """
    #    return Alphabet(self._wrapped(by))

    def __lshift__(self, by):
        """ Shift to the left with the << operator """
        return Alphabet(self._wrapped(by), uniqueify=False)
        
    def __rshift__(self, by):
        """ Shift to the right with the >> operator """
        return Alphabet(self._wrapped(-by), uniqueify=False)
    
    def __repr__(self):
        return repr(''.join((str(e) for e in self)))

    def __len__(self):
        alphabet = self.data
        if not alphabet:
            alphabet = u''
        return len(alphabet)
