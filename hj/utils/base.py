#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict


def _is_stringlike(seq):
    """ Check if a sequence is string-like.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to process.

    Returns
    -------
    `True` if the sequence is string-like, `False` otherwise.

    Notes
    -----
    Testing is done on a slice copy of the sequence since
    a class like `UserString` copies to a plain `str`.

    """
    return isinstance(seq[:], str)


def lrotated(seq, offset):
    """ Left-rotate a copy of the given sequence.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to process.
    offset : int
        Rotate by this number of elements.  Use negative numbers to reverse.
        If greater in magnitude than the length of the sequence,
        a mod operation will be run.

    Returns
    -------
    out : type(seq)
        A processed copy of the given sequence.

    Notes
    -----
    Right-shifting by default would require negating the
    offset values, thus introducing additional complexity.

    """
    try:
        offset %= len(seq)
    except ZeroDivisionError:
        processed = seq[:]  # our API contract promises a copy of `seq`
    else:
        processed = seq[offset:] + seq[:offset]
    return type(seq)(processed)


def screened(seq, mesh):
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
    if _is_stringlike(seq):
        processed = ''.join(processed)
    return type(seq)(processed)


def uniqued(seq):
    """ Remove duplicate elements from a copy of the given sequence.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to process.

    Returns
    -------
    out : type(seq)
        A processed copy of the given sequence.

    """
    processed = OrderedDict.fromkeys(seq)
    if _is_stringlike(seq):
        processed = ''.join(processed)
    return type(seq)(processed)


def keyed(seq, key):
    """ Key a copy of the given sequence.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to process.
    key : sequence
        Prepend this key... [TODO]

    Returns
    -------
    out : type(seq)
        A processed copy of the given sequence.

    Notes
    -----
    Only elements already in this list may be prepended.
    Any resulting duplicates will be handled in the constructor.

    """
    processed = screened(key, seq) + seq
    processed = uniqued(processed)
    return type(seq)(processed)


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
