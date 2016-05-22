#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import itertools
from collections import OrderedDict
from math import gcd
from itertools import zip_longest, cycle, islice


def coprime(a, b):
    """ Determine whether two integers are relatively prime.

    Parameters
    ----------
    a : int
        An integer.
    b : int
        An integer.

    Returns
    -------
    out : bool
        `True` if `a` and `b` are coprime, `False` otherwise.

    Notes
    -----
    The order of the parameters does not matter.

    """
    return gcd(a, b) == 1


# def shares_prime_factors(x, y):
#     c = gcd(x, y)
#     z = y // c
#     while True:
#         if z == 1:
#             return True
#         c = gcd(x, z)
#         if c == 1:
#             return False
#         z = z // c

def prime_sieve(n):
    if n % 2 == 0:
        yield 2

    def divide_out(a, by):
        while a % by == 0:
            a //= by
        return a


    n = divide_out(n, 2)

    i = 3
    while i * i <= n:
        if n % i == 0:
            yield i
            n = divide_out(n, i)
        else:
            i += 2

    for i in range(3, ..., 2):
        pass

    if n > 1:
        yield n

def contains_prime_factors_of(x, y):
    """ does X have all the prime factors of Y?

    Parameters
    ----------
    x : int
        A number to check for shared prime factors.
    y : int
        A number whose prime factors must be in `x`.

    """
    # if result is divisible by somehow reduced-to-unique prime factors number
    # (e.g., 2*2*3*3*5 => x % (2*3*5) == 0), we can return True
    while True:
        # if x % y == 0:  # X divisible by Y, thus Y is GCF of X and Y
        #     return True
        c = gcd(x, y)
        if c == 1:
            return False
        elif c == y:
            return True
        else:
            y //= c

    # print('{}, {}'.format(x, y))

    # c = gcd(x, y)
    # y //= c
    # while True:
    #     print('x, y, gcd = {}, {}, {}'.format(x, y, y*gcd(x, y)))
    #     if y == 1:  # for first step, y //= gcd(x, y) == y indicates that x is multiple of y
    #         return True
    #     c = gcd(x, y)
    #     if c == 1:  # x and y (reduced) are coprime
    #         return False
    #     y //= c

    # while not coprime(x, y):
    #     print('x, y, gcd = {}, {}, {}'.format(x, y, gcd(x, y)))
    #     if x % y == 0:  # if X is divisible by Y, then X is divisible by all prime factors of Y
    #         return True
    #     y //= gcd(x, y)
    # return False

        # if gcd(x, y) == y:  # for first step, y //= gcd(x, y) == y indicates that x is multiple of y
        #     return True
        # 24,8=>8
        # 24,6=>6
        # 24,12
        # ***if x is evenly divisible by y, does that make y the GCD of x and y

        # 14 and 7==> 7 is GCD of 14 and 7
        # 14 and 2==> 2 is GCD of 14 and 2
        # 12 and 8==> 4 is GCD of 12 and 8
    # while True:
    #     print('going through')
    #     if x % y == 0:  # if X is divisible by Y, then X is divisible by all prime factors of Y
    #         return True
    #     # c = gcd(x, y)
    #     if gcd(x, y) == 1:  # x and y (reduced) are coprime
    #         return False
    #     y //= gcd(x, y)


    # while True:
    #     c = gcd(x, y)
    #     if c == 1:  # x and y (reduced) are coprime
    #         return False
    #     y //= c
    #     if y == 1:  # for first step, y //= gcd(x, y) == y indicates that x is multiple of y
    #         return True

    # c = gcd(x, y)
    # y //= c
    # while True:
    #     if y == 1:  # for first step, y //= gcd(x, y) == y indicates that x is multiple of y
    #         return True
    #     c = gcd(x, y)
    #     if c == 1:  # x and y (reduced) are coprime
    #         return False
    #     y //= c


# def finite_ap(start, count, interval):
#     """ Generate a finite arithmetic progression.

#     Parameters
#     ----------
#     start : int
#         The initial term of the sequence.
#     count : int
#         The length of the sequence to generate.
#     interval : int
#         The common difference of the sequence.

#     Returns
#     -------
#     out : generator
#         The resulting sequence as a generator.

#     Notes
#     -----
#     This is essentially just a loose cover for the Python `range` builtin.

#     """
#     return range(start, count * interval + start, interval)


def lcg(m, a, c, seed, limit=None, hull_dobell=True):
    """ Configure a linear congruential generator.

    Parameters
    ----------
    m : int
        The modulus.
    a : int
        The multiplier.
    c : int
        The increment of the sequence.
    seed : int
        The initial term (seed or start value) for the sequence.
    limit : int, optional
        When this is not `None`, only `limit` items will be returned from the
        generator.  Default `None`.
    hull_dobell : bool, optional
        `True` to apply requirements of Hull-Dobell Theorem, `False` otherwise.
        This ensures that the generator has a full period for all seed values.
        Overriding this may result in a less effective PRNG.  Default `True`.

    Returns
    -------
    out : generator
        The resulting infinite sequence as a generator.

    Notes
    -----
    With a multiplier of `1`, this becomes an effective generator for the
    ciphertext alphabet used in the affine cipher.

    [TODO] very much a WIP.  The algorithm appears to work, but input
    validation is lacking, and contains_prime_factors_of() could be clearer.

    [TODO] unit tests very much required

    [TODO] although islice is nice here, I'm not convinced the implementation
    here is ideal, having an inner function accessing outer scope vars,
    as well as combination of `return` and `yield`.

    """
    # if m <= 0:
    #     raise ValueError('Constraint `0 < m` not satisfied.')
    # if m <= a or a <= 0:
    #     raise ValueError('Constraint `0 < a < m` not satisfied.')
    # if m <= c or c < 0:
    #     raise ValueError('Constraint `0 <= c < m` not satisfied.')
    # if m <= seed or seed < 0:
    #     raise ValueError('Constraint `0 <= seed < m` not satisfied.')

    # if not all([ (0 < m), (0 < a < m), (0 <= c < m), (0 <= seed < m) ]):
    #     raise ValueError('hey')

    if hull_dobell:
        if not coprime(m, c):
            raise ValueError('Multiplier and increment must be coprime.')
        if not contains_prime_factors_of(a - 1, m):
            raise ValueError('`m` and `a - 1` must be coprime.')
        if (m % 4) == 0 and (a - 1) % 4 != 0:
            raise ValueError('If `m` is divisible by 4, `a - 1` must be, too.')

    def lcg_():
        out = seed
        while True:
            yield out
            out = (a * out + c) % m

    return itertools.islice(lcg_(), limit)




# def clever_cast(t, s):
#     if t is str:
#         s = ''.join(c for c in s)
#     return t(s)

# def at_modulo(seq, pos):
#     """ Return the element at a given index in sequence, wrapping as needed.
#
#     Parameters
#     ----------
#     seq : sequence
#         A list, tuple, or string to process.
#     pos : int
#         An element index to retrieve.  Will be wrapped if out of bounds.
#
#     Returns
#     -------
#     out : data-type
#         The element at the given index, or `None` if sequence has length 0.
#
#     """
#     try:
#         pos %= len(seq)
#     except ZeroDivisionError:
#         return seq[:]
#     else:
#         return seq[pos]


# def difference(minuend, subtrahend):
#     """ Subtract the characters in one string from those in another.
#
#     Parameters
#     ----------
#     minuend : str
#         A string from which to subtract.
#     subtrahend : str
#         A string to subtract.
#
#     Returns
#     -------
#     out : set
#         An unordered set consisting of remaining characters
#         once `subtrahend` is subtracted from `minuend`.
#     Returns
#     -------
#     out : generator
#         A generator expression for each element in the result.
#
#     Notes
#     -----
#     No apologies are made on the naming conventions for the variables.
#
#     """
#     remainder = set(minuend) - set(subtrahend)
#     return remainder


def lrotated(seq, offset):
    """ Left-rotate a version of the given sequence.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to rotate.
    offset : int
        Rotate this number of elements.  Use negative numbers to reverse.
        If greater in magnitude than the length of the sequence,
        a mod operation will be run.

    Returns
    -------
    out : sequence
        A rotated version of the given sequence.

    Notes
    -----
    Right-shifting by default would require negating the
    offset values, thereby introducing additional complexity.

    """
    try:
        offset %= len(seq)
    except ZeroDivisionError:
        return seq[:]
    else:
        return seq[offset:] + seq[:offset]


def orotated(seq, offset):
    """ Outward-rotate a version of the given sequence.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to rotate.
    offset : int
        Rotate this number of elements.  Use negative numbers to reverse.
        If greater in magnitude than the length of the sequence,
        a mod operation will be run.

    Returns
    -------
    out : sequence
        A rotated version of the given sequence.

    Notes
    -----
    This function acts as though each half of `seq` is on an interlocking gear.

    """
    if len(seq) % 2 != 0:
        raise ValueError('Sequence length must be divisible by two')

    # divide into halves (a first, b second)
    a, b = seq[:len(seq) // 2], seq[len(seq) // 2:]

    # rotate each half symmetrically
    return lrotated(a, offset) + lrotated(b, -offset)

# def index_map(seq):
#     """ Map elements to their indices within a sequence.
#
#     Parameters
#     ----------
#     seq : sequence
#         A sequence to map.
#
#     Return
#     ------
#     out : dict
#         An element-to-index mapping for a sequence.
#
#     """
#     return {element: idx for (idx, element) in enumerate(seq)}


def keyed(seq, key):
    """ Key a copy of the given sequence.

    Parameters
    ----------
    seq : iterable
        A sequence to key with key `key`.
    key : iterable
        A key for the sequencence `seq`.

    Returns
    -------
    out : iterable
        The input sequence `seq`, prefixed with `key`, and only one occurrence
        per character.

    Notes
    -----
    Elements in `key` not already in `seq` will be ignored.
    Repeating characters will be elided to the first occurrence.

    """
    # put valid characters from "key" at beginning of new sequence
    seq_ = [k for k in key if k in seq]

    # add original sequence now
    seq_.extend(seq)

    # eliminate dupes and return
    return OrderedDict.fromkeys(seq_)


# def union(a, b):
#     """ Union of two sequences.
#
#     Parameters
#     ----------
#     a : sequence
#         A list, tuple, or string.
#     b : sequence
#         A list, tuple, or string.
#
#     Returns
#     -------
#     out : set
#         The union of `set(a)` and `set(b)`.
#
#     """
#     return set(a) & set(b)


def grouper(iterable, n, fillvalue=None):
    """ Collect data into fixed-length chunks or blocks.

    Parameters
    ----------
    iterable : iterable
        An iterable to divide into groups.
    n : int
        Group size.
    fillvalue : obj, optional
        Any value to pad empty spaces in the last group.

    Returns
    -------
    out : itertools.zip_longest
        The source iterable divided into groups.

    Notes
    -----
    This comes from the itertools recipes in Python documentation.

    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def roundrobin(*iterables):
    """
    Notes
    -----
    This comes from the itertools recipes in Python documentation.

    """
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def extendable_iterator(seq):
    """ Generator that may be appended to.

    Parameters
    ----------
    seq : iterable
        A sequence or iterator that yields elements.

    Yields
    ------
    out : data-type
        An element from seq.
    in : iterable
        If not falsy, a sequence of elements to append to `seq`.

    Raises
    ------
    TypeError
        If generator input is neither falsy nor iterable.

    """
    seq = list(seq)
    for element in seq:
        food = yield element
        seq.extend(food or [])



def upward_factor(num, factor):
    """ return closest multiple of factor above or equal to num

    Notes
    -----
    [TODO] Needs unit tests.  Also, features using this aren't unit tested.

    """
    return num + factor - 1 - (num - 1) % factor;

def chunks(seq, n):
    """Yield successive n-sized chunks from seq."""
    """ [TODO] note that this raises an exception if n == 0 """
    # adapted from http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    for i in range(0, len(seq), n):
        yield seq[i:i+n]
