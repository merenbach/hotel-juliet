#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import unique
from collections import OrderedDict


class BaseTableau:
    """ Store an alphabet for transcoding.

    Parameters
    ----------
    alphabet : sequence
        An alphabet for the tableau.

    Notes
    -----
    The alphabet need not be string-based.

    [TODO] turn into UserList subclass?

    """
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def __len__(self):
        return len(self.alphabet)

    def __str__(self):
        return str(self.alphabet)


class ZeroDimensionalTableau(BaseTableau):
    """ Tableau with only an alphabet.

    Parameters
    ----------
    alphabet : sequence
        An alphabet for the tableau.  Duplicate elements will be removed.

    """
    def __init__(self, alphabet):
        alphabet = unique(alphabet)
        super().__init__(alphabet)

    def encode(self, s, strict):
        """ Transcode forwards.

        Parameters
        ----------
        s : sequence
            A sequence to transcode.
        strict : bool
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.

        Returns
        -------
        out : sequence
            A transcoded copy of the given sequence `s`.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError

    def decode(self, s, strict):
        """ Transcode backwards.

        Parameters
        ----------
        s : sequence
            A sequence to transcode.
        strict : bool
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.

        Returns
        -------
        out : sequence
            A transcoded copy of the given sequence `s`.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError


class OneDimensionalTableau(ZeroDimensionalTableau):
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

    def _transcode(self, element, strict, table):
        """ Transcode forwards.

        Parameters
        ----------
        element : hashable data-type
            An element to transcode.
        strict : bool
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.  Default `False`.
        table : dict or dict-like
            A dict to handle translation.

        Returns
        -------
        out : data-type
            A transcoded copy (if possible) of the given element `element`.

        Notes
        -----
        If the two alphabets do not have identical character sets, the `strict`
        flag may behave differently based on whether encoding or decoding is
        occurring.  For instance, if this tableau simply converts uppercase to
        lowercase (A => a, B => b) and back again, trying to encode a lowercase
        message (or decode an uppercase one) will result in an empty output
        since no elements were transcodeable.

        """
        default = None
        if not strict:
            default = element
        return table.get(element, default)
        # return map(table.get, element, default)
        # return element.translate(table)

    def encode(self, element, strict):
        """ Transcode forwards.

        Parameters
        ----------
        element : hashable data-type
            An element to transcode.
        strict : bool
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.  Default `False`.

        Returns
        -------
        out : data-type
            A transcoded copy (if possible) of the given element `element`.

        Notes
        -----
        If the two alphabets do not have identical character sets, the `strict`
        flag may behave differently based on whether encoding or decoding is
        occurring.  For instance, if this tableau simply converts uppercase to
        lowercase (A => a, B => b) and back again, trying to encode a lowercase
        message (or decode an uppercase one) will result in an empty output
        since no elements were transcodeable.

        """
        return self._transcode(element, strict, self.a2b)

    def decode(self, element, strict):
        """ Transcode backwards.

        Parameters
        ----------
        element : hashable data-type
            An element to transcode.
        strict : bool
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.  Default `False`.

        Notes
        -----
        If the two alphabets do not have identical character sets, the `strict`
        flag may behave differently based on whether encoding or decoding is
        occurring.  For instance, if this tableau simply converts uppercase to
        lowercase (A => a, B => b) and back again, trying to encode a lowercase
        message (or decode an uppercase one) will result in an empty output
        since no elements were transcodeable.

        Returns
        -------
        out : data-type
            A transcoded copy (if possible) of the given element `element`.

        """
        return self._transcode(element, strict, self.b2a)


class TwoDimensionalTableau(ZeroDimensionalTableau):
    """ Polyalphabetic tableau.

    Parameters
    ----------
    alphabet : sequence
        An alphabet for the tableau.  Duplicate elements will be removed.
    alphabets_ : sequence
        An iterable of alphabets.

    """
    def __init__(self, alphabet, alphabets_):
        super().__init__(alphabet)
        self.alphabets_ = alphabets_
    #
    # #     alphabets = self._make_rows(alphabet)
    # #     transcoders_list = [Transcoder(alphabet, ab_) for ab_ in alphabets]
    # #     self.alphabets_ = OrderedDict(zip(keys or alphabet, transcoders_list))
    # #     self.alphabet_ = unique(alphabet_)
    # #     self.a2b = dict(zip(alphabet, alphabet_))
    # #     self.b2a = dict(zip(alphabet_, alphabet))
    # #     # self.a2b = str.maketrans(alphabet, alphabet_)
    # #     # self.b2a = str.maketrans(alphabet_, alphabet)

    def encode(self, element, key, strict):
        """ Locate element within the grid.

        Parameters
        ----------
        element : str
            An element to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.
        strict : bool
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.

        Returns
        -------
        out : data-type
            A transcoded copy (if possible) of the given element `element`.

        Raises
        ------
        KeyError
            If no tableau could be found for the given key.

        """
        transcoder = self.alphabets_[key]
        return transcoder.encode(element, strict)

    def decode(self, element, key, strict):
        """ Locate element within the grid.

        Parameters
        ----------
        element : str
            An element to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.
        strict : bool
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.

        Returns
        -------
        out : data-type
            A transcoded copy (if possible) of the given element `element`.

        Raises
        ------
        KeyError
            If no tableau could be found for the given key.

        """
        transcoder = self.alphabets_[key]
        return transcoder.decode(element, strict)
