#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict


class OneWayTranslationTable:
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
    def __init__(self, pt, ct):
        self.a2b = str.maketrans(pt, ct)
        self.pt, self.ct = pt, ct

    def __len__(self):
        return len(self.a2b)

    def __str__(self):
        base = type(self).__name__
        pt = 'PT: {}'.format(self.pt)
        ct = 'CT: {}'.format(self.ct)
        return '{}\n  {}\n  {}'.format(base, pt, ct)

    def __repr__(self):
        return '{}: {} => {}'.format(type(self).__name__,
                                     repr(self.pt),
                                     repr(self.ct))

    def encode(self, s):
        """ Transcode forwards.

        Parameters
        ----------
        s : str
            A string to transcode.

        Returns
        -------
        out : str
            A transcoded version of `s`.

        """
        return s.translate(self.a2b)


class TwoWayTranslationTable(OneWayTranslationTable):
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

    def decode(self, s):
        """ Transcode backwards.

        Parameters
        ----------
        s : str
            A string to transcode.

        Returns
        -------
        out : str
            A transcoded version of `s`.

        """
        return s.translate(self.b2a)
