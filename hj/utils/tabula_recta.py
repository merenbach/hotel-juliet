#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .alphabet import Alphabet
from .transcoder import Transcoder
from .base import index_map


# [TODO] make this a subclass of alphabet instead of BaseTabula?
# or are the manipulation aspects silly?  might make it easier to rotate
# and do keyed cipher stuff
class TabulaRecta:
    """ Message alphabet is on top; key alphabet is on side.

    Parameters
    ----------
    alphabet : str or string like, optional
        An alphabet to use for transcoding.

    """
    def __init__(self, alphabet=None):
        alphabet = Alphabet(alphabet)
        # tcharmap, icharmap = {}, {}
        transcoders = {}
        for i, c in enumerate(alphabet):
            alphabet_ = alphabet.lrotate(i)
            transcoders[c] = Transcoder(alphabet, alphabet_)
        self.transcoders = transcoders

        # [TODO] kludgy vars that shouldn't be here
        self.msg_alphabet = alphabet
        self.key_alphabet = alphabet

    # [TODO] give generic names to params here (one is definitely edge,
    # while another can be edge or inside, depending on direction)
    def transcode(self, a, b, intersect=False):
        """ Locate element within the grid.

        Parameters
        ----------
        a : str
            A character in the alphabet.
        b : str
            A character in the alphabet.
        intersect : bool, optional
            `True` to find character at intersection of `k` and `m`.
            `False` to work back from `k` and intersection `m` to find edge.
            Default `False`.

        Returns
        -------
        out : str
            The transcoded character in the message alphabet.

        """
        key_charmap = self.transcoders.get(b, None)
        if key_charmap:
            if intersect:
                return key_charmap.encode(a)
            else:
                return key_charmap.decode(a)

        if not intersect:  # or if intersect, if rotated by -n above
            return a.translate(self.icharmap[b])
        else:
            return a.translate(self.tcharmap[b])
        # try:
        #     x, y = self.charmap[a], self.charmap[b]
        # except KeyError:
        #     return None
        # else:
        #     pos = x + y if intersect else x - y
        #     element = self.alphabet.at(pos)
        #     return str(element)

    # def __repr__(self):
    #     return repr(self.alphabet)
    #     # alphabet = self.alphabet
    #     #
    #     # rows = [self.alphabet << n for n in range(len(alphabet))]
    #     # keyed_rows = dict(zip(self.alphabet_, rows))
    #     # lines = []
    #     # lines.append('    ' + ' '.join(str(alphabet)))
    #     # lines.append('')
    #
    #     for k in self.alphabet_:
    #         row = ' '.join(str(keyed_rows[k]))
    #         lines.append('{0}   {1}   {0}'.format(k, row))
    #
    #     lines.append('')
    #     lines.append('    ' + ' '.join(str(alphabet)))
    #
    #     return '\n'.join(lines)
