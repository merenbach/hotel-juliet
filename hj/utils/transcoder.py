from .base import difference
from collections import namedtuple, UserString


class Transcoder:
    """ Convert strings between two character sets.

    Parameters
    ----------
    a : str
        A source character set.
    b : str
        A destination character set.

    """
    def __init__(self, a, b):
        self._a = self._b = None  # initialize underlying ivars
        # self.a, self.b = a, b
        self.a = str(a) if isinstance(a, UserString) else a  # maketrans needs str
        self.b = str(b) if isinstance(b, UserString) else b  # maketrans needs str

    def encode(self, s):
        return s.translate(self.a2b)

    def decode(self, s):
        return s.translate(self.b2a)

    def _update(self):
        """ Update translator cache.

        Raises
        ------
        TypeError
            If either `self.a` or `self.b` is not a string.
        ValueError
            If `self.a` and `self.b` have unequal length.

        """
        a, b = self.a, self.b
        if a and b:
            self.a2b, self.b2a = str.maketrans(a, b), str.maketrans(b, a)
        else:
            self.a2b = self.b2a = None

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value
        self._update()

    @a.deleter
    def a(self):
        del self._a
        self._update()

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value
        self._update()

    @b.deleter
    def b(self):
        del self._b
        self._update()

    def __str__(self):
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
        # this methodology may be flawed: only one alphabet should probably
        # be checked (`a`?) as the input/message alphabet
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
