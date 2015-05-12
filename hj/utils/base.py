#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# from collections import OrderedDict
from fractions import gcd
# from collections import UserString


def _recast(seq, out):
    """ Recast sequence `out` as type of sequence `seq`.

    Parameters
    ----------
    seq : sequence
        Get the type of this sequence.
    out : sequence
        Cast this sequence.

    Returns
    -------
    out : type(seq)
        A cast copy of of `out` as type of `seq`.

    """
    # if isinstance(seq, (str, UserString)):
    if isinstance(seq[:], str):
        out = ''.join(out)
    return type(seq)(out)


def _screened(seq, mesh):
    """ Filter elements from a copy of the given sequence.

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
    processed = [e for e in seq if e in mesh]
    return _recast(seq, processed)


def testscreened(seq, mesh):
    return _screened(seq, mesh)


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

# def flipped(sequence):
#     """ Reverse the given sequence.

#         Parameters
#         ----------
#         sequence : sequence
#             A sequence (string, list, etc.) to process.

#         Returns
#         -------
#         A reversed copy of the sequence.

#     """
#     return sequence[::-1]
#     # return list(reversed(sequence))
