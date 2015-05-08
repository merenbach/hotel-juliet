# -*- coding: utf-8 -*-

# from collections import OrderedDict


def lrotated(seq, offset):
    """ Left-rotate a copy of the given sequence.

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
    out : type(seq)
        A rotated copy of the given sequence.

    Notes
    -----
    Right-shifting by default would require negating the
    offset values, thus introducing additional complexity.

    """
    # [TODO]? if abs(offset) > len(seq):
    # [TODO]? if seq:
    if len(seq) > 0:
        offset %= len(seq)
    # our API contract promises a copy even if len(seq) == 0
    rotated = seq[offset:] + seq[:offset]
    return type(seq)(rotated)


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
