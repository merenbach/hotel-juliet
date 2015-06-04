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

    [TODO] turn into UserList subclass?

    """
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def __len__(self):
        return len(self.alphabet)

    def __str__(self):
        return str(self.alphabet)

    def contains(self, element):
        """ Does this tableau contain a given character?

        Parameters
        ----------
        element : data-type
            Check this tableau for this character.

        Returns
        -------
        out : bool
            `True` if the element exists in this tableau, `False` otherwise.

        Notes
        -----
        This equates with "can transcode": provided this returns `True`,
        this tableau should be able to transcode the given character.

        Some subclasses (e.g., key-based tableaux like the tabula recta)
        may impose additional restrictions.

        """
        return element in self.alphabet


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

    def encode(self, s, strict=False):
        """ Transcode forwards.

        Parameters
        ----------
        s : sequence
            A sequence to transcode.
        strict : bool, optional
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.  Default `False`.

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

    def decode(self, s, strict=False):
        """ Transcode backwards.

        Parameters
        ----------
        s : sequence
            A sequence to transcode.
        strict : bool, optional
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.  Default `False`.

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

    def _transcode(self, s, xtable, lenient):
        out = (xtable.get(c, lenient and c) for c in s)
        return [c for c in out if c]

    def encode(self, s, strict=False):
        """ Transcode forwards.

        Parameters
        ----------
        s : sequence
            A sequence to transcode.
        strict : bool, optional
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.  Default `False`.

        Returns
        -------
        out : sequence
            A transcoded copy of the given sequence `s`.

        """
        return self._transcode(s, self.a2b, not strict)
        # return map(self.a2b.get, s, s)
        # return s.translate(self.a2b)

    def decode(self, s, strict=False):
        """ Transcode backwards.

        Parameters
        ----------
        s : sequence
            A sequence to transcode.
        strict : bool, optional
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.  Default `False`.

        Returns
        -------
        out : sequence
            A transcoded copy of the given sequence `s`.

        """
        return self._transcode(s, self.b2a, not strict)
        # return map(self.b2a.get, s, s)
        # return s.translate(self.b2a)


class TwoDimensionalTableau(OneDimensionalTableau):
    """ Polyalphabetic tableau.

    Parameters
    ----------
    alphabet : sequence
        An alphabet for the tableau.  Duplicate elements will be removed.
    tableaux : sequence of `OneDimensionalTableau`
        Rows for the tableau.

    """
    # def __init__(self, alphabet, tableaux):
    #     from string import ascii_uppercase
    #     from utils import lrotated
    #     t = [OneDimensionalTableau(alphabet, lrotated(ascii_uppercase, n)) for n in range(26)]
    #     super().__init__(alphabet, t)
    #
    # #     alphabets = self._make_rows(alphabet)
    # #     transcoders_list = [Transcoder(alphabet, ab_) for ab_ in alphabets]
    # #     self.data = OrderedDict(zip(keys or alphabet, transcoders_list))
    # #     self.alphabet_ = unique(alphabet_)
    # #     self.a2b = dict(zip(alphabet, alphabet_))
    # #     self.b2a = dict(zip(alphabet_, alphabet))
    # #     # self.a2b = str.maketrans(alphabet, alphabet_)
    # #     # self.b2a = str.maketrans(alphabet_, alphabet)

    def encode(self, s, key, strict=False):
        """ Locate element within the grid.

        Parameters
        ----------
        s : str
            A string to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.
        strict : bool, optional
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.  Default `False`.

        Returns
        -------
        out : str
            An encoded string, or `None` if no key transcoder could be found.

        Raises
        ------
        KeyError
            If no tableau could be found for the given key.

        """
        transcoder = self.data[key]
        return transcoder.encode(s, strict=strict)

    def decode(self, s, key, strict=False):
        """ Locate element within the grid.

        Parameters
        ----------
        s : str
            A string to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.
        strict : bool, optional
            `False` to return non-transcodable elements unchanged,
            `True` to replace with `None`.  Default `False`.

        Returns
        -------
        out : str
            A decoded string, or `None` if no key transcoder could be found.

        Raises
        ------
        KeyError
            If no tableau could be found for the given key.

        """
        transcoder = self.data[key]
        return transcoder.decode(s, strict=strict)
