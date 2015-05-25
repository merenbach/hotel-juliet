#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .transcoder import Transcoder
from collections import OrderedDict
# from string import digits
from .base import lrotated, orotated


# class BaseTableau:
#     """ Base class for encoding and decoding operations.
#
#     """
#     # def __init__(self):
#     #     pass
#
#     def encode(self, s):
#         """ Transcode forwards.
#
#         Parameters
#         ----------
#         s : sequence
#             A sequence to encode.
#
#         Returns
#         -------
#         out : sequence
#             An encoded copy of the given sequence `s`.
#
#         Raises
#         ------
#         NotImplementedError
#             If not overridden.
#
#         """
#         raise NotImplementedError
#
#     def decode(self, s):
#         """ Transcode backwards.
#
#         Parameters
#         ----------
#         s : sequence
#             A sequence to decode.
#
#         Returns
#         -------
#         out : sequence
#             A decoded copy of the given sequence `s`.
#
#         Raises
#         ------
#         NotImplementedError
#             If not overridden.
#
#         """
#         raise NotImplementedError


class BaseTabulaRecta:
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    transcoders : dict
        A dictionary mapping keys to Transcoder objects.

    """
    def __init__(self, transcoders):
        self.transcoders = OrderedDict(transcoders)

    def encode(self, s, xkey):
        """ Locate element within the grid.

        Parameters
        ----------
        s : str
            A string to transcode.
            Essentially a row header character on the left edge of the tableau.
        xkey : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.

        Returns
        -------
        out : str
            An encoded string, or `None` if no key transcoder could be found.

        """
        transcoder = self.transcoders.get(xkey)
        return transcoder and transcoder.encode(s)

    def decode(self, s, xkey):
        """ Locate element within the grid.

        Parameters
        ----------
        s : str
            A string to transcode.
            Essentially a row header character on the left edge of the tableau.
        xkey : str
            The dictionary key of a transcoder.
            Essentially a row header character on the left edge of the tableau.

        Returns
        -------
        out : str
            A decoded string, or `None` if no key transcoder could be found.

        """
        transcoder = self.transcoders.get(xkey)
        return transcoder and transcoder.decode(s)


# class Tabula(BaseTabula):
#     """ A tabula fit for a monoalphabetic cipher.
#   [TODO] could do one of these for each type of mono cipher, thus deferring
#    responsibility of generating alphabets.
#
#     Parameters
#     ----------
#     alphabet : str or string like
#         A plaintext alphabet to use for transcoding.
#     alphabet_ : str or string like
#         An enciphered alphabet to use for transcoding.
#
#     """
#     def __init__(self, alphabet, alphabet_):
#         transcoder = Transcoder(alphabet, alphabet_)
#         super().__init__(transcoders={None: transcoder})
#         # [TODO] could also run: self.transcoders.update({None: transcoder})
#
#     def __repr__(self):
#         return repr(self.transcoders[None])


class TabulaRecta(BaseTabulaRecta):
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    alphabet : str or string like, optional
        An alphabet to use for transcoding.
    keys : sequence
        An ordered sequence of keys to use for generated transcoders.

    """
    def __init__(self, charset, keys=None):
        self.charset = charset
        alphabets = self._make_rows(charset)
        transcoders_list = [Transcoder(charset, ab_) for ab_ in alphabets]
        transcoders = zip(keys or charset, transcoders_list)
        super().__init__(transcoders)

    def __repr__(self):
        charset = self.charset
        lines = []
        lines.append('  | ' + ' '.join(charset))
        lines.append('--+' + '-' * len(charset) * 2)
        for k, v in self.transcoders.items():
            row = ' '.join(v.b)
            lines.append('{0} | {1}'.format(k, row))
        return '\n'.join(lines)

    def _make_rows(self, charset):
        """ Create alphabets.

        Returns
        -------
        out : list
            An ordered collection of character sets.

        """
        return [lrotated(charset, i) for i in range(len(charset))]
        # return [lrotated(charset, i) for i, _ in enumerate(charset)]


class BeaufortTabulaRecta(TabulaRecta):
    """ Beaufort cipher version.

    """
    def _make_rows(self, charset):
        return super()._make_rows(charset[::-1])


class PortaTabulaRecta(TabulaRecta):
    """ Porta cipher version, doubling up rows and symmetrically rotating.

    [TODO] Would like to be able to make fewer overrides on parent class logic,
    as well as more nicely represent the tableau in __repr__, say with
    either collapsed rows... or with keys equal to
    [('A', 'B'), ('C', 'D'), ... ('Y', 'Z')] and a "search" function
    to find the right one before passing to super.

    """
    def __repr__(self):
        charset = self.charset[:len(self.charset) // 2]
        lines = []
        lines.append('     | ' + ' '.join(charset))
        lines.append('-----+' + '-' * len(charset) * 2)
        i = 0
        cur_l = ''
        for k, v in self.transcoders.items():
            row = ' '.join(v.b[:len(charset)])
            if i % 2 == 0:
                cur_l= k
            elif i % 2 == 1:
                cur_l+=', '+k
                lines.append('{0} | {1}'.format(cur_l, row))
            i += 1
        return '\n'.join(lines)

    def _make_rows(self, charset):
        charset = lrotated(charset, len(charset) // 2)
        return [orotated(charset, i // 2) for i in range(len(charset))]

# [TODO] class GronsfeldTabulaRecta, etc.?

    #
    #     # [TODO] kludgy vars that shouldn't be here
    #     # self.msg_alphabet = alphabet
    #     # self.keys = alphabet
    #
    #     # try:
    #     #     x, y = self.charmap[a], self.charmap[b]
    #     # except KeyError:
    #     #     return None
    #     # else:
    #     #     pos = x + y if intersect else x - y
    #     #     element = self.alphabet.at(pos)
    #     #     return str(element)
    #
    # def _make_transcoders(self):
    #     """ [TODO] these docs aren't current
    #     Create a transcoding alphabet.
    #
    #     Returns
    #     -------
    #     out : sequence
    #         A transformed alphabet.
    #
    #     Raises
    #     ------
    #     NotImplementedError
    #         If not overridden.
    #
    #     Notes
    #     -----
    #     Since this is invoked by `__init__()` before instance is totally
    #     initialized, please don't perform any operations that expect a fully
    #     constructed instance.
    #
    #     """
    #     raise NotImplementedError

