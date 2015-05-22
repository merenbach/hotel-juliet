#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SubCipher
from utils.transcoder import Transcoder


class MonoSubCipher(SubCipher):
    """ Monoalphabetic substitution transcoder.

    """
    def _make_tableau(self, charset):
        charset_ = self._transform(charset)
        return Transcoder(charset, charset_)

    def _transform(self, charset):
        """ Transform a character set for transcoding.

        Parameters
        ----------
        charset : str
            A character set to use for transcoding.

        Returns
        -------
        out : str
            A transformed version of the provided character set.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError

    def _encode(self, s):
        return self.tableau.encode(s)

    def _decode(self, s):
        return self.tableau.decode(s)
