#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict


class CipherTableau:
    """ Metadata used at least to determine substitution input/output charsets.

    Parameters
    ----------
    pt : str
        A plaintext alphabet for the tableau.
    ct : str
        A ciphertext alphabet for the tableau.

    """
    def __init__(self, pt, ct):
        self.pt, self.ct = pt, ct

    def __repr__(self):
        return '{}: PT=[{}], CT=[{}]'.format(type(self).__name__,
                                             repr(self.pt),
                                             repr(self.ct))

    def __str__(self):
        return 'PT: {}\nCT: {}'.format(self.pt, self.ct)


class ManyToOneTranslationTable(CipherTableau):
    """ Monoalphabetic tableau.

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
        super().__init__(pt, ct)
        self.a2b = str.maketrans(pt, ct)

    def __len__(self):
        return len(self.a2b)

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


class OneToOneTranslationTable(ManyToOneTranslationTable):
    """ Reciprocal monoalphabetic tableau.

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
