#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from fractions import gcd
# from collections import UserString


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


def testscreened(seq, mesh):
    """ Filter elements from a copy of the given sequence.

    [todo] ***ONLY USED IN ONE PLACE, FOR STRICT TRANSCODING***

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to process.
    mesh : sequence
        Filter the original sequence through this sequence.
        Only elements also in `mesh` will be retained in the output.
        If an item is in `mesh` but not in `seq`, it is ignored.

    Returns
    -------
    out : type(seq)
        A processed copy of the given sequence.

    """
    return [e for e in seq if e in mesh]


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
