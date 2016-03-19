#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from utils import upward_factor


class ManyToOneTranslationTable:
    """ Monoalphabetic tableau.

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

    Notes
    -----
    Recurring symbols in `plaintext` may yield undefined output when encoding.

    The ciphertext alphabet may contain reccurences, for instance in the case
    of homophonic substitution ciphers, where multiple ciphertext symbols may
    represent a single plaintext symbol.  (In this case, recurrences simply
    means characters repeated at least once, whether consecutive or not.)

    """
    DEFAULT_NULLCHAR = 'X'

    def __init__(self, pt, ct):
        self.a2b = str.maketrans(pt, ct)
        self.pt, self.ct = pt, ct

    def __len__(self):
        return len(self.a2b)

    def __str__(self):
        return 'PT: {}\nCT: {}'.format(self.pt, self.ct)

    def __repr__(self):
        return '{}: {} => {}'.format(type(self).__name__,
                                     repr(self.pt),
                                     repr(self.ct))

    def encode(self, s, block=None):
        """ Transcode forwards.

        Parameters
        ----------
        s : str
            A string to transcode.
        strict : bool
            `True` to strip out non-transcodable characters, `False` otherwise.

        Returns
        -------
        out : str
            A transcoded version of `s`.

        """
        if block is not None:
            s = ''.join(c for c in s if c in self.pt)

            if block > 0:
                padding = upward_factor(len(s), block)
                s = s.ljust(padding, self.DEFAULT_NULLCHAR)

        return s.translate(self.a2b)


class OneToOneTranslationTable(ManyToOneTranslationTable):
    """ Monoalphabetic tableau.

    Parameters
    ----------
    pt : sequence
        A plaintext alphabet for the tableau.
    ct : sequence
        A ciphertext alphabet for the tableau.

    Notes
    -----
    Recurring symbols in `plaintext` or `ciphertext` may yield undefined output
    when encoding or decoding.

    Because standard reverse substitution requires a one-to-one mapping,
    homophonic substitution ciphers are not currently supported in a two-way
    fashion.  Technically some heuristics could be devised, such as randomly
    choosing one of several ciphertext characters for each individual plaintext
    character.  [TODO]?

    """
    def __init__(self, pt, ct):
        super().__init__(pt, ct)
        self.b2a = str.maketrans(ct, pt)

    def __repr__(self):
        return '{}: {} <=> {}'.format(type(self).__name__,
                                      repr(self.pt),
                                      repr(self.ct))

    def decode(self, s, block=None):
        """ Transcode backwards.

        Parameters
        ----------
        s : str
            A string to transcode.
        strict : bool
            `True` to strip out non-transcodable characters, `False` otherwise.

        Returns
        -------
        out : str
            A transcoded version of `s`.

        """
        if block is not None:
            s = ''.join(c for c in s if c in self.pt)

        out = s.translate(self.b2a)

        if block is not None and block > 0:
            padding = upward_factor(len(out), block)
            out = out.ljust(padding, self.DEFAULT_NULLCHAR)

        return out
