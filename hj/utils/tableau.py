#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import unique


class CipherTableau:
    """ Metadata used at least to determine substitution input/output charsets.

    Parameters
    ----------
    pt : str
        A plaintext alphabet for the tableau.
    ct : str
        A ciphertext alphabet for the tableau.

    Raises
    ------
    ValueError
        If `pt` and `ct` have different lengths.

    """
    def __init__(self, pt, ct):
        if len(pt) != len(ct):
            raise ValueError('Both alphabets must have the same length.')
        self.pt, self.ct = pt, ct

    @staticmethod
    def transpose(element, source, target, offset=0):
        """ Shift an element between alphabets based off of its index.

        Parameters
        ----------
        element : object
            An element to transcode.
        source : sequence
            A source character set (e.g., plaintext alphabet).
        target : sequence
            A target character set (e.g., ciphertext alphabet).
        offset : int, optional
            Shift the element over this number of characters à la Caesar shift.
            Default `0`.

        Returns
        -------
        out : object
            A transcoded copy (if possible) of the given element `element`.

        Raises
        ------
        ValueError
            If no index in `source` could be found for the given element.
        ZeroDivisionError
            If length of `target` is zero.

        Notes
        -----
        This may underlie both monoalphabetic and polyalphabetic substitution.
        Intriguingly, replacing the call to `str.index` with one to `str.find`
        yields a curiously inadvertent implementation of null characters, which
        show up as `offset - 1` (since `str.find` returns `-1` on not found).

        Also note that in many other coding languages, we'd probably want to
        add len(target) to `n` before running a modulo operation to ensure
        that `n` would be a positive integer.  Modular arithmethic on negatives
        may differ by some implementations, so perhaps it should be added.
        [TODO]

        """
        n = source.index(element) + offset  # + len(target)
        return target[n % len(target)]

    def __repr__(self):
        return '{}: PT=[{}], CT=[{}]'.format(type(self).__name__,
                                             repr(self.pt), repr(self.ct))

    def __str__(self):
        return 'PT: {}\nCT: {}'.format(self.pt, self.ct)


class ManyToOneTranslationTable(CipherTableau):
    """ Monoalphabetic tableau.

    Notes
    -----
    Recurring symbols in `plaintext` will be ignored.

    The ciphertext alphabet may contain recurrences, for instance in the case
    of homophonic substitution ciphers, where multiple ciphertext symbols may
    represent a single plaintext symbol.  (In this case, recurrences simply
    means characters repeated at least once, whether consecutive or not.)

    """
    DEFAULT_NULLCHAR = 'X'

    def __init__(self, pt, ct):
        super().__init__(unique(pt), ct)

    def __repr__(self):
        return '{}: {} => {}'.format(type(self).__name__,
                                     repr(self.pt), repr(self.ct))

    def encipher(self, element):
        """ Transcode forwards.

        Parameters
        ----------
        element : object
            An element to transcode.

        Returns
        -------
        out : object
            A transcoded version of `element`, or the non-transcoded `element`
            if transcoding failed.

        """
        try:
            return self.transpose(element, self.pt, self.ct)
        except ValueError:
            return element


class OneToOneTranslationTable(ManyToOneTranslationTable):
    """ Reciprocal monoalphabetic tableau.

    Notes
    -----
    Recurring symbols in `plaintext` or `ciphertext` will be ignored.

    Because standard reverse substitution requires a one-to-one mapping,
    homophonic substitution ciphers are not currently supported in a two-way
    fashion.  Technically some heuristics could be devised, such as randomly
    choosing one of several ciphertext characters for each individual plaintext
    character.  [TODO]?

    """
    def __init__(self, pt, ct):
        super().__init__(pt, unique(ct))

    def __repr__(self):
        return '{}: {} <=> {}'.format(type(self).__name__,
                                      repr(self.pt), repr(self.ct))

    def decipher(self, element):
        """ Transcode backwards.

        Parameters
        ----------
        element : object
            An element to transcode.

        Returns
        -------
        out : object
            A transcoded version of `element`, or the non-transcoded `element`
            if transcoding failed.

        """
        try:
            return self.transpose(element, self.ct, self.pt)
        except ValueError:
            return element
