#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from fractions import gcd
from itertools import zip_longest


def at_modulo(seq, pos):
    """ Return the element at a given index in sequence, wrapping as needed.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to process.
    pos : int
        An element index to retrieve.  Will be wrapped if out of bounds.

    Returns
    -------
    out : data-type
        The element at the given index, or `None` if sequence has length 0.

    """
    try:
        pos %= len(seq)
    except ZeroDivisionError:
        return seq[:]
    else:
        return seq[pos]


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
    offset values, thus introducing additional complexity.

    """
    try:
        offset %= len(seq)
    except ZeroDivisionError:
        return seq[:]
    else:
        return seq[offset:] + seq[:offset]


def index_map(seq):
    """ Map elements to their indices within a sequence.

    Parameters
    ----------
    seq : sequence
        A sequence to map.

    Return
    ------
    out : dict
        An element-to-index mapping for a sequence.

    """
    return {element: idx for (idx, element) in enumerate(seq)}


def multiplied(seq, by):
    """ Multiply each element's position by a number.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to rotate.
    by : int
        A number by which to multiply each element's position.

    Returns
    -------
    out : generator
        The resulting sequence as a generator.

    Raises
    ------
    ValueError
        If `by` and `len(seq)` are not coprime.

    Notes
    -----
    [TODO]: Make this more elegant.

    """
    self_len = len(seq)
    if not coprime(by, self_len):
        raise ValueError('Multiplier and alphabet length must be coprime.')

    positions = [(by * n) % self_len for n in range(self_len)]
    return (seq[n] for n in positions)


def unique(seq):
    """ Get unique items in sequence, preserving order.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to process.

    Returns
    -------
    out : generator
        A generator expression for each element in the result.

    """
    return (n for n in OrderedDict.fromkeys(seq))


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
