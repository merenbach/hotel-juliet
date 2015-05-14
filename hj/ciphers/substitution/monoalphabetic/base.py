#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils.alphabet import Alphabet


class BaseMonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : sequence
        A source (plaintext) alphabet to underlie transcoding.

    Raises
    ------
    ValueError
        If `alphabet` and `alphabet_` have unequal length.

    """
    def __init__(self, alphabet):
        alphabet_ = self.make_alphabet_(alphabet)
        if len(alphabet) != len(alphabet_):
            raise ValueError('Alphabets must have equal length')
        self.alphabet, self.alphabet_ = alphabet, alphabet_
        self.xtable, self.xtable_ = self._make_xtables(alphabet, alphabet_)
        super().__init__()

    def _make_xtable(self, a, b):
        """ Create translation tables for encoding.

        Parameters
        ----------
        a : str or string like
            The source alphabet.
        b : str or string like
            The destination alphabet.

        Returns
        -------
        out : dict
            A string translation table.

        Raises
        ------
        ValueError
            If `a` and `b` have unequal length.

        """
        return str.maketrans(str(a), str(b))

    def _make_xtables(self, a, b):
        """ Create translation tables for encoding.

        Parameters
        ----------
        a : str or string like
            The source alphabet.
        b : str or string like
            The destination alphabet.

        Returns
        -------
        out : tuple(dict, dict)
            Inverse translation tables.

        Raises
        ------
        ValueError
            If `a` and `b` have unequal length.

        """
        xtable = self._make_xtable(a, b)
        xtable_ = self._make_xtable(b, a)
        return xtable, xtable_

    def make_alphabet_(self, alphabet):
        """ Create a transcoding alphabet.

        Parameters
        ----------
        alphabet : sequence
            An alphabet to transform.

        Returns
        -------
        out : sequence
            A transformed alphabet.

        Raises
        ------
        NotImplementedError
            If not overridden.

        Notes
        -----
        Since this is invoked by `__init__()` before instance is totally
        initialized, please don't perform any operations that expect a fully
        constructed instance.

        """
        raise NotImplementedError

    def _encode(self, s, strict):
        s = super()._encode(s, strict)
        return s.translate(self.xtable)

    def _decode(self, s, strict):
        s = super()._decode(s, strict)
        return s.translate(self.xtable_)

    # def _transcode(self, s, strict=False, reverse=False):
    #     """ Convert elements within a sequence.

    #     Parameters
    #     ----------
    #     s : sequence
    #         A sequence to encode.
    #     strict : bool, optional
    #         `True` to strip all characters not in this cipher's alphabet,
    #         `False` to funnel through to output.  Defaults to `False`.

    #     Returns
    #     -------
    #     out : sequence
    #         A transcoded message.

    #     """
    #     if strict:
    #         from utils.base import testscreened
    #         s = testscreened(s, self.alphabet)
    #     return s


class MonoSubCipher(BaseMonoSubCipher):
    """ Monoalphabetic substitution transcoder.

    Parameters
    ----------
    alphabet : str or string like, optional
        A source (plaintext) alphabet to underlie transcoding.  Default `None`.
        If you cannot afford one, one will
        be provided for you at no cost to you.

    Notes
    -----
    The `BaseMonoSubCipher` class may be initialized with sequences of
    any sort.  This subclass assumes existence of the Alphabet utility
    class, so for philosophical reasons it is separated out here.

    """
    def __init__(self, alphabet=None):
        alphabet = Alphabet(alphabet)
        super().__init__(alphabet)

    def __repr__(self):
        return '{}\n{}'.format(self.alphabet, self.alphabet_)


    # def _transcode(self, s, strict=False, xtable=None, block=0):
    #     """ Convert elements within a sequence.
    #
    #     Parameters
    #     ----------
    #     s : sequence
    #         A sequence to transcode.
    #     strict : bool, optional
    #         `True` to strip all characters not in this cipher's alphabet,
    #         `False` to funnel through to output.  Defaults to `False`.
    #     reverse : bool, optional
    #         `True` to transcode in the forwards direction, `False` to transcode
    #         backwards.  Defaults to `False`.
    #
    #     Returns
    #     -------
    #     out : sequence
    #         A transcoded message.
    #
    #     """
    #     # s = super()._transcode(s, strict=strict, reverse=reverse)
    #     if strict:
    #         from utils.base import testscreened
    #         s = testscreened(s, self.alphabet)
    #     return s.translate(xtable)
