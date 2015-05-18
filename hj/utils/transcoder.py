from .alphabet import Alphabet
from .base import difference


class BaseTranscoder:
    """ Convert sequences between two character sets.

    Parameters
    ----------
    a : sequence
        A source character set.
    b : sequence
        A destination character set.

    Raises
    ------
    ValueError
        If `a` and `b` have unequal length.

    """
    def __init__(self, a, b):
        if len(a) != len(b):
            raise ValueError('Character sets must have equal length')
        self.a, self.b = a, b
        # self.a_to_b = {i: j for i, j in zip(a, b)}
        # self.b_to_a = {i: j for i, j in zip(b, a)}
        # (self.a[c] for c in s)
        # (self.b[c] for c in s)

    def encode(self, s):
        """ Convert a string from character set `a` to character set `b`.

        Parameters
        ----------
        s : sequence
            A sequence to encode.

        Returns
        -------
        out : str
            The encoded sequence.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError

    def decode(self, s):
        """ Convert a string from character set `b` to character set `a`.

        Parameters
        ----------
        s : sequence
            A sequence to decode.

        Returns
        -------
        out : str
            The decoded sequence.

        Raises
        ------
        NotImplementedError
            If not overridden.

        """
        raise NotImplementedError


class Transcoder(BaseTranscoder):
    """ Convert strings between two character sets.

    Parameters
    ----------
    a : str or string like
        A source character set.
    b : str or string like
        A destination character set.

    Raises
    ------
    ValueError
        If `a` and `b` have unequal length.

    """
    def __init__(self, a, b):
        a, b = str(a), str(b)
        super().__init__(a, b)
        self.a_to_b = str.maketrans(self.a, self.b)
        self.b_to_a = str.maketrans(self.b, self.a)

    def __repr__(self):
        return '{}\n{}'.format(self.a, self.b)

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
        orphans = difference(s, self.a + self.b)
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

    def encode(self, s):
        """ Convert a string from character set `a` to character set `b`.

        Parameters
        ----------
        s : str
            A string to encode.

        Returns
        -------
        out : str
            The encoded string.

        """
        # xtable = str.maketrans(self.a_to_b)
        return s.translate(self.a_to_b)

    def decode(self, s):
        """ Convert a string from character set `b` to character set `a`.

        Parameters
        ----------
        s : str
            A string to decode.

        Returns
        -------
        out : str
            The decoded string.

        """
        # xtable = str.maketrans(self.b_to_a)
        return s.translate(self.b_to_a)
