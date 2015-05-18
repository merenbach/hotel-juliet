#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .alphabet import Alphabet
from .transcoder import Transcoder
from .base import index_map


class BaseTabula:
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    transcoders : dict
        A dictionary mapping keys to Transcoder objects.

    """
    def __init__(self, transcoders=None):
        self.transcoders = transcoders or {}

    def encode(self, s, xkey=None):
        """ Locate element within the grid.

        Parameters
        ----------
        s : str
            A string to transcode.
            Essentially a row header character on the left edge of the tableau.
        xkey : str, optional
            The dictionary key of a transcoder.  Default `None`.
            Essentially a row header character on the left edge of the tableau.

        Returns
        -------
        out : str
            An encoded string, or `None` if no key transcoder could be found.

        """
        try:
            transcoder = self.transcoders[xkey]
        except KeyError:
            return None
        else:
            return transcoder.encode(s)

    def decode(self, s, xkey=None):
        """ Locate element within the grid.

        Parameters
        ----------
        s : str
            A string to transcode.
            Essentially a row header character on the left edge of the tableau.
        xkey : str, optional
            The dictionary key of a transcoder.  Default `None`.
            Essentially a row header character on the left edge of the tableau.

        Returns
        -------
        out : str
            A decoded string, or `None` if no key transcoder could be found.

        """
        try:
            transcoder = self.transcoders[xkey]
        except KeyError:
            return None
        else:
            return transcoder.decode(s)


class Tabula(BaseTabula):
    """ A tabula fit for a monoalphabetic cipher.

    Parameters
    ----------
    alphabet : str or string like
        A plaintext alphabet to use for transcoding.
    alphabet_ : str or string like
        An enciphered alphabet to use for transcoding.

    """
    def __init__(self, alphabet, alphabet_):
        transcoder = Transcoder(alphabet, alphabet_)
        super().__init__(transcoders={None: transcoder})
        # [TODO] could also run: self.transcoders.update({None: transcoder})

    def __repr__(self):
        return repr(self.transcoders[None])


class TabulaRecta(BaseTabula):
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    alphabet : str or string like, optional
        An alphabet to use for transcoding.

    """
    def __init__(self, alphabet=None):
        alphabet = Alphabet(alphabet)
        transcoders = self._make_transcoders(alphabet)
        super().__init__(transcoders=transcoders)

        # [TODO] kludgy vars that shouldn't be here
        self.msg_alphabet = alphabet
        self.key_alphabet = alphabet

        # try:
        #     x, y = self.charmap[a], self.charmap[b]
        # except KeyError:
        #     return None
        # else:
        #     pos = x + y if intersect else x - y
        #     element = self.alphabet.at(pos)
        #     return str(element)

    def _make_transcoders(self):
        """ [TODO] these docs aren't current
        Create a transcoding alphabet.

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


    def _make_transcoders(self, alphabet):
        transcoders = {}
        for i, c in enumerate(alphabet):
            alphabet_ = alphabet.lrotate(i)
            transcoders[c] = Transcoder(alphabet, alphabet_)
        return transcoders

    def __repr__(self):
        alphabet = self
        return str(alphabet)

        rows = [alphabet << n for n in range(len(alphabet))]
        keyed_rows = dict(zip(self, rows))
        lines = []
        lines.append('    ' + ' '.join(str(alphabet)))
        lines.append('')

        for k in str(self):
            row = ' '.join(str(keyed_rows[k]))
            lines.append('{0}   {1}   {0}'.format(k, row))

        lines.append('')
        lines.append('    ' + ' '.join(str(alphabet)))

        return '\n'.join(lines)
