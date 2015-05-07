# -*- coding: utf-8 -*-

from collections import OrderedDict


def rotated(seq, offset):
    """ Wrap a copy (left shifted) of the given sequence.

    Parameters
    ----------
    seq : sequence
        A list, tuple, or string to process.
    offset : int
        Rotate by this offset.  Use negative numbers to reverse.
        If greater in magnitude than the length of the sequence,
        a mod operation will be run.

    Returns
    -------
    A wrapped copy of the sequence.

    Notes
    -----
    Right-shifting would require negating the offset values,
    which introduces additional complexity.

    """
    if len(seq) > 0:
        offset %= len(seq)
        seq = seq[offset:] + seq[:offset]
    return seq


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


# def uniqued(seq):
#     """ Remove duplicate elements from the given sequence.

#         Parameters
#         ----------
#         seq : sequence
#             A list, tuple, or string to process.

#         Returns
#         -------
#         A "uniquified" copy of the sequence.

#     """
#     d = OrderedDict.fromkeys(seq)
#     # [TODO] this part is a kludge
#     if isinstance(seq, str):
#         d = ''.join(d)
#     return type(seq)(d)
