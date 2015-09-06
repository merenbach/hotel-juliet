#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import unique_list, transform_with_dict


class MonoalphabeticTableau(object):
    """ Monoalphabetic tableau.

    Parameters
    ----------
    a : sequence
        A source map for the tableau.  Duplicate elements will be removed.
    b : sequence
        A target map for the tableau.  Duplicate elements will be removed.

    Notes
    -----
    The `encode` and `decode` methods, in conjunction with the `a2b` and `b2a`
    dictionaries, function very much like `str.translate` with the output of
    `str.maketrans`.  An alternative implementation is included, commented-out,
    for anyone interested.

    """
    def __init__(self, a, b):
        a, b = unique_list(a), unique_list(b)
        if len(a) != len(b):
            raise ValueError('the first two parameters must have equal length')
            # raise ValueError('the first two parameters must have equal number '
            #                  'of distinct elements')
        self.a, self.b = a, b
        self.a2b, self.b2a = dict(zip(a, b)), dict(zip(b, a))
        # self.a2b = str.maketrans(alphabet, alphabet_)
        # self.b2a = str.maketrans(alphabet_, alphabet)

    def __str__(self):
        return 'PT: {}\nCT: {}'.format(self.a, self.b)

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

        """
        return transform_with_dict(self.a2b, element, strict)

    def decode(self, element, strict):
        """ Transcode backwards.

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

        """
        return transform_with_dict(self.b2a, element, strict)


class TwoDimensionalTableau(object):
    """ Polyalphabetic tableau.

    Parameters
    ----------
    alphabet : sequence
        An alphabet for the tableau.  Duplicate elements will be removed.
    alphabets_ : sequence
        An iterable of alphabets.

    """
    def __init__(self, alphabet, alphabets_):
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
