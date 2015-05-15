#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils.alphabet import Alphabet, AlphabetTranscoder


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
        self._validate_alphabet(alphabet)
        alphabet_ = self.make_alphabet_(alphabet)
        self.transcoder = AlphabetTranscoder(alphabet, alphabet_)
        super().__init__()

    def __repr__(self):
        return repr(self.transcoder)

    def _validate_alphabet(self, alphabet):
        """ [TODO] remove me... """
        pass

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
        if strict:
            s = self.transcoder.sanitize(s)
        s = super()._encode(s)
        return self.transcoder.encode(s)

    def _decode(self, s, strict):
        if strict:
            s = self.transcoder.sanitize(s)
        s = super()._decode(s)
        return self.transcoder.decode(s)

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
