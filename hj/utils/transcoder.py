from .alphabet import Alphabet


class BaseTranscoder:
    """ Convert between two alphabets.

    Parameters
    ----------
    a : str or string like
        A source character set.
    b : str or string like
        A destination character set.

    """
    def __init__(self, a, b):
        self.a, self.b = str(a), str(b)

    def __repr__(self):
        return '{}\n{}'.format(self.a, self.b)

    def encode(self, s, strict=False):
        """ Convert a string from character set `a` to character set `b`.

        Parameters
        ----------
        s : str
            A string to encode.
        strict : bool, optional
            `True` to cut from output any non-transcodeable characters,
            `False` to leave them untouched.  Default `False`.

        Returns
        -------
        out : str
            The encoded string.

        """
        return self._transcode(s, self.a, self.b, strict)

    def decode(self, s, strict=False):
        """ Convert a string from character set `b` to character set `a`.

        Parameters
        ----------
        s : str
            A string to encode.
        strict : bool, optional
            `True` to cut from output any non-transcodeable characters,
            `False` to leave them untouched.  Default `False`.

        Returns
        -------
        out : str
            The encoded string.

        """
        return self._transcode(s, self.b, self.a, strict)

    def _transcode(self, s, src, dst, strict):
        """ Convert a string from character set `b` to character set `a`.

        Parameters
        ----------
        s : str
            A string to transcode.
        src : str
            A source character set.
        dst : str
            A destination character set.
        strict : bool
            `True` to cut from output any non-transcodeable characters,
            `False` to leave them untouched.

        Returns
        -------
        out : str
            The transcoded string.

        """
        cut = strict and ''.join({s} - {src + dst})
        xtable = str.maketrans(src, dst, cut or '')
        return s.translate(xtable)

    # def _xtable(self, src, dst):
    #     """ Create a translation table between alphabets.
    #
    #     Parameters
    #     ----------
    #     src : str
    #         A source alphabet.
    #     dst : str
    #         A destination alphabet.
    #
    #     Returns
    #     -------
    #     out : dict
    #         A translation table suitable for `str.translate()`.
    #
    #     Raises
    #     ------
    #     TypeError
    #         If either `src` or `dst` is `None`.
    #     ValueError
    #         If `src` and `dst` have unequal length.
    #
    #     """
    #     return str.maketrans(src, dst)


class Transcoder(BaseTranscoder):
    """ Transcode between two alphabets.

    Raises
    ------
    ValueError
        If `a` and `b` have unequal length.

    """
    def __init__(self, a, b):
        a, b = Alphabet(a), Alphabet(b)
        if len(a) != len(b):
            raise ValueError('Alphabets must have equal length')
        super().__init__(a, b)

    def encode(self, s, strict=False):
        """ Convert a string from character set `a` to character set `b`.

        Parameters
        ----------
        s : str
            A string to encode.
        strict : bool, optional
            `True` to cut from output any non-transcodeable characters,
            `False` to leave them untouched.

        Returns
        -------
        out : str
            The encoded string.

        """
        return self._transcode(s, self.a, self.b, strict=strict)

    def decode(self, s, strict=False):
        """ Convert a string from character set `b` to character set `a`.

        Parameters
        ----------
        s : str
            A string to encode.

        Returns
        -------
        out : str
            The encoded string.

        """
        return self._transcode(s, self.b, self.a, strict=strict)

    def _orphans(self, s):
        """ Find "orphaned" characters in a message.

        Parameters
        ----------
        s : str or string-like
            A string to check for non-processable characters.

        Returns
        -------
        out : str
            Characters that can't be transcoded.

        """
        print('***_ORPHANS MAY BE DEPRECATED')
        orphans = set(s) - set(self.a + self.b)
        return ''.join(orphans)

    def sanitize(self, s):
        """ Strip "orphaned" characters from a message.

        Parameters
        ----------
        s : str or string-like
            A string to sanitize of non-processable characters.

        Returns
        -------
        out : str
            The original string.

        """
        print('***sanitize MAY BE DEPRECATED')
        orphans = self._orphans(s)
        xtable = str.maketrans('', '', orphans)
        return s.translate(xtable)
