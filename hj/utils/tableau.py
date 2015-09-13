#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import TranscoderStream, unique_list

# # [TODO]--instead of passing "strict" around, how about just returning a
# wrapper for the non-transcodeable element and the original caller can
# determine what to do with it?


# class TranslationTable:
#     def __init__(self, xtable):
#         """ xtable is a dict"""
#         self.xtable = xtable
#
#     def _transform(self, element, strict):
#         try:
#             return self.xtable[element]
#         except KeyError:
#             if not strict:
#                 return element
#             else:
#                 raise
#
#     def transform(self, element, strict):
#         return self._transform(element, strict)
#
#
# class NonTranscodeableElement:
#     """ Mark elements that could not be transcoded; what happens to these is at
#         the presentation layer.
#
#     """
#     def __init__(self, element):
#         self.element = element


class MonoalphabeticTableau:
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
    dictionaries, function similarly to `str.maketrans` with `str.translate`.

    """
    def __init__(self, a, b):
        self.a2b, self.b2a = TranscoderStream(a, b), TranscoderStream(b, a)

    def __str__(self):
        return self.a2b.p(delimiter=',\n ', keyvalsep=' <=> ')

    def __repr__(self):
        return repr(self.a2b)

    def encode(self, seq, strict):
        """ Transcode forwards.

        Parameters
        ----------
        seq : iterable
            An iterable of elements to transcode.

        Returns
        -------
        out : data-type
            The transcoded counterparts, if possible, of the input sequence.

        """
        return self.a2b.transcode(seq, strict)

    def decode(self, seq, strict):
        """ Transcode backwards.

        Parameters
        ----------
        seq : iterable
            An iterable of elements to transcode.

        Returns
        -------
        out : data-type
            The transcoded counterparts, if possible, of the input sequence.

        """
        return self.b2a.transcode(seq, strict)


class TwoDimensionalTableau:
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

    def encode(self, seq, key):
        """ Locate element within the grid.

        Parameters
        ----------
        element : str
            An element to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.

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
        return transcoder.encode(seq, True)

    def decode(self, seq, key):
        """ Locate element within the grid.

        Parameters
        ----------
        element : str
            An element to transcode.
            Essentially a row header character on the left edge of the tableau.
        key : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.

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
        return transcoder.decode(seq, True)
