#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import unique


class BaseTableau:
    """ Store an alphabet for transcoding.

    Parameters
    ----------
    alphabet : sequence
        An alphabet for the tableau.

    Notes
    -----
    The alphabet need not be string-based.

    """
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def __len__(self):
        return len(self.alphabet)

    def __str__(self):
        return str(self.alphabet)


class Tableau(BaseTableau):
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    alphabet : sequence
        An alphabet for the tableau.  Duplicate elements will be removed.

    """
    def __init__(self, alphabet):
        alphabet = unique(alphabet)
        super().__init__(alphabet)

    def encode(self, s):
        """ Transcode forwards.

        Parameters
        ----------
        s : sequence
            A sequence to encode.

        Returns
        -------
        out : sequence
            An encoded copy of the given sequence `s`.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError

    def decode(self, s):
        """ Transcode backwards.

        Parameters
        ----------
        s : sequence
            A sequence to decode.

        Returns
        -------
        out : sequence
            A decoded copy of the given sequence `s`.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError


class OneDimensionalTableau(Tableau):
    """ Monoalphabetic tableau.

    Parameters
    ----------
    alphabet : sequence
        An alphabet for the tableau.  Duplicate elements will be removed.
    alphabet_ : sequence
        An alphabet for the tableau.  Duplicate elements will be removed.

    Notes
    -----
    The `encode` and `decode` methods, in conjunction with the `a2b` and `b2a`
    dictionaries, function very much like `str.translate` with the output of
    `str.maketrans`.  An alternative implementation is included, commented-out,
    for anyone interested.

    """
    def __init__(self, alphabet, alphabet_):
        super().__init__(alphabet)
        self.alphabet_ = unique(alphabet_)
        self.a2b = dict(zip(alphabet, alphabet_))
        self.b2a = dict(zip(alphabet_, alphabet))
        # self.a2b = str.maketrans(alphabet, alphabet_)
        # self.b2a = str.maketrans(alphabet_, alphabet)

    def __str__(self):
        return 'PT: {}\nCT: {}'.format(self.alphabet, self.alphabet_)

    def encode(self, s):
        """ Transcode forwards.

        Parameters
        ----------
        s : sequence
            A sequence to encode.

        Returns
        -------
        out : sequence
            An encoded copy of the given sequence `s`.
            Non-encodable elements will be included unchanged.

        """
        return [self.a2b.get(c, c) for c in s]
        # return s.translate(self.a2b)

    def decode(self, s):
        """ Transcode backwards.

        Parameters
        ----------
        s : sequence
            A sequence to decode.

        Returns
        -------
        out : sequence
            A decoded copy of the given sequence `s`.
            Non-decodable elements will be included unchanged.

        """
        return [self.b2a.get(c, c) for c in s]
        # return s.translate(self.b2a)


class TwoDimensionalTableau(Tableau):
    """ Polyalphabetic tableau.

    Parameters
    ----------
    alphabet : sequence
        An alphabet for the tableau.  Duplicate elements will be removed.

    """
    def encode(self, s, key):
        """ Locate element within the grid.

        Parameters
        ----------
        s : str
            A string to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.

        Returns
        -------
        out : str
            An encoded string, or `None` if no key transcoder could be found.

        """
        transcoder = self.data.get(key)
        return transcoder and transcoder.encode(s)

    def decode(self, s, key):
        """ Locate element within the grid.

        Parameters
        ----------
        s : str
            A string to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.

        Returns
        -------
        out : str
            A decoded string, or `None` if no key transcoder could be found.

        """
        transcoder = self.data.get(key)
        return transcoder and transcoder.decode(s)
