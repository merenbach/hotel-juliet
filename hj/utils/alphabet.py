#!/usr/bin/python
# -*- coding: utf-8 -*-

import string

class Alphabet(object):
    """
    Attributes
    ----------
    DEFAULT_ALPHABET : str
                       A Unicode string of characters to use when none are specified.
                       Alphabets may make use of non-string sequences for their members.
    """
    DEFAULT_ALPHABET = unicode(string.ascii_uppercase)
    
    """ Represent a string of unique characters """
    def __init__(self, elements=None, uniqueify=True, nullchar=None):
        if not elements:
            # If no alphabet is specified, use a "default" of ASCII uppercase
            elements = self.DEFAULT_ALPHABET
        # Ensure that characters are unique
        if uniqueify:
            # Render the characters within the alphabet unique prior to storing them
            self.elements = tuple(c for i, c in enumerate(elements) if not c in elements[:i])
        else:
            self.elements = tuple(elements)
    
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
            return self.elements[i]
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
            return self.elements.index(c)
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
        
        return affine_transform(self.elements, m, b, inverse=inverse)

    def reversed(self):
        """ Return a reversed version of this alphabet """
        return Alphabet(self._reversed(), uniqueify=False)
        
    def _reversed(self):
        """ Return a reversed version of this alphabet as a string """
        return self.elements[::-1]

    def keyed(self, keyword):
        """ Return a "codeword" version of this alphabet """
        return Alphabet(self._keyed(keyword=keyword), uniqueify=True)

    def _keyed(self, keyword):
        """ Return a "codeword" version of this alphabet as a string """
        # Restrict keyword to characters already in the alphabet
        # This helps to prevent inadvertent "extension" of the alphabet
        # This is more efficient but uniquifying throws an error
        #return Uniqueifier().uniqueify([c for c in keyword if c in self.elements] + self.elements)
        return self.common(tuple(keyword)) + self.elements

    def _wrapped(self, offset):
        """ Return a wrapped copy (left shifted) of this alphabet as a string """
        o = self.elements
        if len(o) > 0:
            offset %= len(o)
            o = o[offset:] + o[:offset]
        return o

    def common(self, s):
        """ Return a supplied string stripped of characters not in this alphabet """
        f = lambda c: c in self.elements
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
        return repr(u''.join((str(e) for e in self.elements)))

    def __len__(self):
        alphabet = self.elements
        if not alphabet:
            alphabet = u''
        return len(alphabet)