#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .alphabet import Alphabet
from .transcoder import Transcoder
from .base import index_map


# [TODO] make this a subclass of alphabet instead of BaseTabula?
# or are the manipulation aspects silly?  might make it easier to rotate
# and do keyed cipher stuff
class TabulaRecta(Alphabet):
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    alphabet : str or string like, optional
        An alphabet to use for transcoding.

    """
    def __init__(self, alphabet=None):
        super().__init__(alphabet)
        alphabet = Alphabet(alphabet)
        transcoders = {}
        for i, c in enumerate(alphabet):
            alphabet_ = alphabet.lrotate(i)
            transcoders[c] = Transcoder(alphabet, alphabet_)
        self.transcoders = transcoders

        # [TODO] kludgy vars that shouldn't be here
        self.msg_alphabet = alphabet
        self.key_alphabet = alphabet

    def transcode(self, a, b, intersect=False):
        """ Locate element within the grid.

        Parameters
        ----------
        a : str
            A header character on the edge of the tableau.
        b : str
            A header character on the edge of the tableau,
            or a character within (if `intersect` is `True`).
        intersect : bool, optional
            `True` to look for the intersection of `a` and `b`, `False` to
            look for the edge location that intersects with `a` to form `b`.
            Default `False`.

        Returns
        -------
        out : str
            The transcoded character in the message alphabet.

        """
        try:
            transcoder = self.transcoders[a]
        except KeyError:
            return None
        else:
            # f = transcoder.encode if intersect else transcoder.decode
            # return f(b, strict=True)
            if intersect:
                return transcoder.encode(b)
            else:
                return transcoder.decode(b)
        # try:
        #     x, y = self.charmap[a], self.charmap[b]
        # except KeyError:
        #     return None
        # else:
        #     pos = x + y if intersect else x - y
        #     element = self.alphabet.at(pos)
        #     return str(element)

    def __repr__(self):
        # return repr(self.alphabet)
        alphabet = self

        rows = [alphabet << n for n in range(len(alphabet))]
        keyed_rows = dict(zip(self, rows))
        lines = []
        lines.append('    ' + ' '.join(str(alphabet)))
        lines.append('')

        for k in self:
            row = ' '.join(str(keyed_rows[k]))
            lines.append('{0}   {1}   {0}'.format(k, row))

        lines.append('')
        lines.append('    ' + ' '.join(str(alphabet)))

        return '\n'.join(lines)
