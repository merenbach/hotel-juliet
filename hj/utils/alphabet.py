# -*- coding: utf-8 -*-

import string
from collections import UserList, OrderedDict


class BaseAlphabet(UserList):
    """ Base alphabet class with only unique elements in initlist.

    """
    def __init__(self, initlist=None):
        initlist = OrderedDict.fromkeys(initlist)
        super().__init__(initlist=initlist)

    def __lshift__(self, by):
        """ Shift to the left with the << operator.

        """
        print('*** OPERATOR OVERLOADING MAY BE DEPRECATED')
        return self.rotated(by)

    def __rshift__(self, by):
        """ Shift to the right with the >> operator.

        """
        print('*** OPERATOR OVERLOADING MAY BE DEPRECATED')
        return self.rotated(-by)

    def reversed(self):
        """ Reverse a copy of this list.

        Returns
        -------
        out : type(self)
            A reversed copy of this list.

        """
        initlist = reversed(self)
        return type(self)(initlist)

    def rotated(self, offset):
        """ Rotate a copy (left shifted) of this list.

        Parameters
        ----------
        offset : int
            Rotate by this offset.  Use negative numbers to reverse.
            If greater in magnitude than the length of the sequence,
            a mod operation will be run.

        Returns
        -------
        out : type(self)
            A rotated copy of this list.

        Notes
        -----
        Right-shifting would require negating the offset values,
        which introduces additional complexity.

        """
        initlist = self
        if len(initlist) > 0:
            offset %= len(initlist)
            initlist = initlist[offset:] + initlist[:offset]
        return type(self)(initlist)

    def keyed(self, key):
        """ Key a copy of this list.

        Parameters
        ----------
        seq : sequence
            A sequence with which to key this list.

        Notes
        -----
        Only elements already in this list may be prepended.
        Any resulting duplicates will be handled in the constructor.

        """
        initlist = [c for c in key if c in self] + self
        return type(self)(initlist)


class Alphabet(BaseAlphabet):
    """
    Attributes
    ----------
    DEFAULT_ALPHABET : str
        A Unicode string of characters to use when none are specified.
        Alphabets may make use of non-string sequences for their members.

    """
    DEFAULT_ALPHABET = string.ascii_uppercase
    
    """ Represent a string of unique characters """
    def __init__(self, initlist=None):
        # If no alphabet is specified, use a "default" of ASCII uppercase
        if not initlist:
            initlist = self.DEFAULT_ALPHABET
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

    def affinal(self, m, b, inverse=False):
        return Alphabet(self._affinal(m, b, inverse=inverse))
    
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

    def common(self, s):
        """ Return a supplied string stripped of characters not in this alphabet """
        print('**** ALPHABET.COMMON WILL BE DEPRECATED')
        f = lambda c: c in self.data
        return filter(f, s)
    
    # def __repr__(self):
    #     return repr(''.join((str(e) for e in self)))
