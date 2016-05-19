#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
from collections import OrderedDict
from math import gcd
from itertools import zip_longest, cycle, islice


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


def multiplied(seq, m, b):
    """ Multiply each element's position by a number.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to multiply (the multiplicand).
    m : int
        A number by which to multiply each element's position (the multiplier).
    b : int
        A number to add to the multiplication of element positions.

    Returns
    -------
    out : generator
        The resulting sequence as a generator.

    Raises
    ------
    ValueError
        If `by` and `len(seq)` are not coprime.

    """
    seq_len = len(seq)
    if not coprime(m, seq_len):
        raise ValueError('Multiplier and alphabet length must be coprime.')

    return (seq[n % seq_len] for n in range(b, seq_len * m, m))
    # positions = [(m * n + b) for n in range(seq_len)]
    # return (seq[n % seq_len] for n in positions)


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


def coprime(a, b):
    """ Determine whether `a` and `b` are coprime.

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

    """
    return gcd(a, b) == 1


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
    """ return closest multiple of factor above or equal to num """
    return num + factor - 1 - (num - 1) % factor;

def chunks(seq, n):
    """Yield successive n-sized chunks from seq."""
    """ [TODO] note that this raises an exception if n == 0 """
    # adapted from http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    for i in range(0, len(seq), n):
        yield seq[i:i+n]
