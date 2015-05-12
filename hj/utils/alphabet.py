#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from collections import OrderedDict, UserString


class AlphabetOperation:
    """ Perform a manipulation on an alphabet object.

    """
    pass


class AlphabetKeyOperation(AlphabetOperation):
    def __init__(self, keyword):
        self.keyword = keyword

    def handle(self, a):
        return a.keyed(self.keyword)
        # if not reverse:
        #     return a << self.shift
        # else:
        #     return a >> self.shift


class AlphabetShiftOperation(AlphabetOperation):
    def __init__(self, shift):
        self.shift = shift

    def handle(self, a):
        return a << self.shift
        # if not reverse:
        #     return a << self.shift
        # else:
        #     return a >> self.shift


class AlphabetReverseOperation(AlphabetOperation):
    def handle(self, a):
        return ~a


# class AlphabetSequence(UserList):
#     def __init__(self, alphabet, initlist=None):
#         self.alphabet = alphabet
#         super().__init__(initlist=initlist)

#     def alphabet1(self):
#         return self.alphabet

#     def alphabet2(self):
#         a = self.alphabet
#         for op in self:
#             a = op.handle(a)
#         return a


class FlexibleSequenceMixin:
    """ Extended methods for sequence (UserString, UserList) flexibility.

    Notes
    -----
    This mixin should be added only to sequence-like such as `str`, `list`,
    `tuple`, `UserString`, `UserList`, etc.  Failure to adhere to these
    instructions may result in undefined behavior.

    The point of this class is to abstract out robust methods for type-agnostic
    sequence manipulation, the ultimate objective being support for non-string
    alphabets (think encoding by tuples, integers, etc.), which is both totally
    pointless and conceptually awesome.

    """
    def _reversed(self):
        """ Reverse a version of this sequence.

        Returns
        -------
        out : sequence
            A reversed copy of this sequence.

        Notes
        -----
        The `reversed` class provides a way to reverse arbitrary sequences.
        Because it provides a generator, using it on strings requires logic
        in `_recast()` that may be less robust or harder to test for now.

        """
        return self[::-1]

    def _lrotated(self, offset):
        """ Left-rotate a version of this sequence.

        Parameters
        ----------
        offset : int
            Rotate this number of elements.  Use negative numbers to reverse.
            If greater in magnitude than the length of the sequence,
            a mod operation will be run.

        Returns
        -------
        out : sequence
            A rotated version of this sequence.

        Notes
        -----
        Right-shifting by default would require negating the
        offset values, thus introducing additional complexity.

        """
        try:
            offset %= len(self)
        except ZeroDivisionError:
            return self
        else:
            return self[offset:] + self[:offset]

    def __lshift__(self, by):
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
        seq = self._lrotated(by)
        return self._recast(seq)

    def __rshift__(self, by):
        """ Shift a copy of this sequence to the right with the >> operator.

        Parameters
        ----------
        by : int
            Shift by this many elements.

        Returns
        -------
        out : type(self)
            A right-shifted copy of this sequence.

        """
        seq = self._lrotated(-by)
        return self._recast(seq)

    def __invert__(self):
        """ Reverse a copy of this sequence.

        Returns
        -------
        out : type(self)
            A reversed copy of this sequence.

        """
        seq = self._reversed()
        return self._recast(seq)

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

        """
        return type(self)(seq)


class BaseAlphabet(UserString, FlexibleSequenceMixin):
    """ Base alphabet class with uniqueness requirement. """
    def __init__(self, seq):
        seq = ''.join(OrderedDict.fromkeys(str(seq)))
        super().__init__(seq)

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

    def _recast(self, seq):
        """ Recast a sequence as type of self.

        Notes
        -----
        Add mechanism to flatten sequence of strings.

        """
        # if isinstance(self, (str, UserString)):
        if str(self) == self:
            # str() call works around inability to join list of UserStrings
            seq = ''.join(str(s) for s in seq)
        return super()._recast(seq)


# def joinit(self, seq, stringlike=False):
#     processed = OrderedDict.fromkeys(seq)
#     if stringlike:
#         processed = ''.join(processed)
#     return type(self)(processed)

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

    """
    DEFAULT_ALPHABET = string.ascii_uppercase

    """ Represent a string of unique characters """
    def __init__(self, seq=None):
        # If no alphabet is specified, use a "default" of ASCII uppercase
        if not seq:
            seq = self.DEFAULT_ALPHABET
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

# Subclasses for each cipher?  Then rotate/key/etc. in init()...

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
