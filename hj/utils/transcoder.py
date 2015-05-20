from .base import difference
from collections import namedtuple, UserString


class Transcoder(namedtuple('Transcoder', 'a b encode decode')):
    """ Convert strings between two character sets.

    """
    __slots__ = ()

    def __new__(cls, a, b):
        """
        Parameters
        ----------
        cls : data-type
            Boilerplate.
        a : str
            A source character set.
        b : str
            A destination character set.

        """
        a = str(a) if isinstance(a, UserString) else a  # maketrans needs str
        b = str(b) if isinstance(b, UserString) else b  # maketrans needs str
        a2b, b2a = str.maketrans(a, b), str.maketrans(b, a)
        encode = lambda s: s.translate(a2b)  # cache translation table
        decode = lambda s: s.translate(b2a)  # cache translation table
        return super().__new__(cls, a, b, encode, decode)

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
