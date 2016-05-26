#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import itertools
import math
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
        `True` if `a` and `b` share no prime factors, `False` otherwise.

    Notes
    -----
    The order of the parameters does not matter.

    """
    return math.gcd(a, b) == 1


def divisible(a, b):
    """ Determine whether one integer evenly divides another.

    Parameters
    ----------
    a : int
        A dividend.
    b : int
        A divisor.

    Returns
    -------
    out : bool
        `True` if `a` is evenly divisible by `b` `False` otherwise.

    """
    return (a % b) == 0


def regular(a, b):
    """ Do all the prime factors of `a` also divide `b`?

    Parameters
    ----------
    a : int
        An integer whose prime factors are being divided into `b`.
    b : int
        An integer into which to attempt to divide the prime factors of `a`.

    Returns
    -------
    `True` if `a` is `b`-regular, `False` otherwise.

    Raises
    ------
    ValueError
        If `a` == 0.

    Notes
    -----
    Definition of "regularity" coming from Michael Thomas De Vlieger,
      <http://www.vincico.com/proof/neutral.html>.

    See also: <https://oeis.org/A243103>

    """
    if a == 0:
        raise ValueError('Parameter `a` must be nonzero.')

    while b != 1:
        b = math.gcd(b, a)
        a //= b
    return a == 1


def lcg(m, a, c, seed, hull_dobell=True):
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
    hull_dobell : bool, optional
        `True` to apply requirements of Hull-Dobell Theorem, `False` otherwise.
        This ensures that the generator has a full period for all seed values.
        Overriding this may result in a less effective PRNG.  Default `True`.

    Yields
    ------
    out : int
        The resulting infinite sequence as a generator.

    Notes
    -----
    With a multiplier of `1`, this becomes an effective generator for the
    ciphertext alphabet used in the affine cipher.

    [TODO] needs more input validation

    [TODO] unit tests very much required

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
        if not regular(m, a - 1):
            raise ValueError('Prime factors of `m` must also divide `a - 1`.')
        if divisible(m, 4) and not divisible(a - 1, 4):
            raise ValueError('If 4 divides `m`, 4 must divide `a - 1`.')

    while True:
        yield seed
        seed = (seed * a + c) % m


def intersect(a, b):
    """ Intersect two sequences.

    Parameters
    ----------
    a : sequence
        An iterable to filter.  Order will be preserved.
    b : sequence
        Only retain elements in `a` if they exist in this iterable.

    Returns
    -------
    out : list
        All the elements from `a`, minus any that don't appear in `b`.

    """
    return [e for e in a if e in b]


def unique(seq, prefix=[]):
    """ Filter recurrences in a sequence, optionally rearranging.

    Parameters
    ----------
    seq : sequence
        A sequence to condense.
    prefix : iterable, optional
        A forced prefix for this sequence.
        Elements not already in `seq` will be ignored.
        Defaults to an empty list.

    Returns
    -------
    out : list
        The input sequence `seq`, prefixed optionally with `prefix`, and only
        the first occurrence of each character retained.

    Notes
    -----
    [TODO] needs unit tests

    """
    d = collections.OrderedDict.fromkeys(seq)
    for k in reversed(prefix):
        try:
            d.move_to_end(k, last=False)
        except KeyError:
            pass
    return list(d.keys())


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



def upward_factor(factor, base):
    """ return closest multiple of factor above or equal to num

    Parameters
    ----------
    factor : int
    base : int

    Notes
    -----
    [TODO] features using this aren't fully unit tested

    """
    return base + factor - 1 - (base - 1) % factor;


def chunks(seq, n):
    """Yield successive n-sized chunks from seq."""
    """ [TODO] note that this raises an exception if n == 0 """
    # adapted from http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    for i in range(0, len(seq), n):
        yield seq[i:i+n]
