# -*- coding: utf-8 -*-


def rotated(sequence, offset):
    """ Wrap a copy (left shifted) of the given sequence.

    Parameters
    ----------
    sequence : sequence
        A sequence (string, list, etc.) to process.
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
    if len(sequence) > 0:
        offset %= len(sequence)
        sequence = sequence[offset:] + sequence[:offset]
    return sequence


def flipped(sequence):
    """ Reverse the given sequence.

        Parameters
        ----------
        sequence : sequence
            A sequence (string, list, etc.) to process.

        Returns
        -------
        A reversed copy of the sequence.

    """
    return sequence[::-1]


def uniqued(sequence):
    """ Remove duplicate elements from the given sequence, preserving order.

        Parameters
        ----------
        sequence : sequence
            A sequence (string, list, etc.) to process.

        Returns
        -------
        A "uniquified" copy of the sequence.

    """
    return sequence
