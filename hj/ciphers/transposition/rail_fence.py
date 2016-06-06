#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import TransCipher
from utils import *
import utils
import itertools
from collections import defaultdict, Counter, OrderedDict

# NULLCHAR = 'X'
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))


class OrderedCounter(Counter, OrderedDict):
    'Counter that remembers the order elements are first encountered'

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)



class RailFenceCipher(TransCipher):
    """ Transcode based on a numeric shift.

    Parameters
    ----------
    key : int
        The count of rails in the fence.
    alphabet : str, optional
        A character set to use for transcoding.  Default `None`.

    Notes
    -----
    This is far less polished than the other ciphers.  Given time...

    .... should be able to print tableau....

        # should have blocks, strict, etc. from sub ciphers


    """
    def __init__(self, key, nullchar=None, alphabet=None):
        self.nullchar = nullchar or self.DEFAULT_NULLCHAR
        super().__init__(key, alphabet=alphabet)

    def _encode(self, s):
        rails = OrderedDict()
        z = utils.zigzag(range(self.key))
        for char, rail in zip(s, z):
            rails.setdefault(rail, []).append(char)
        out = itertools.chain.from_iterable(rails.values())
        return ''.join(out)

    def _fence(self, s):
        rails = OrderedDict()
        z = utils.zigzag(range(self.key))
        for key in range(self.key):
            rails.setdefault(key, [])
        keys = list(range(self.key))
        for char, rail in zip(s, z):
            for k in keys:
                if k != rail:
                    rails[k].append('.')
                else:
                    rails[k].append(char)
        out = (' '.join(val) for val in rails.values())
        return '\n'.join(out)
        # out = itertools.chain.from_iterable(rails.values())
        # return ''.join(out)

        ####### we need a generator for 0,1,2,1,0,1,2,1....
        ####### to translate into rail 1,2,3,2,1,2,3....
        ### one implementation, but not correct, because it's more of a stripe/
        # regrouping algo, as opposed to the zig-zag that is req'd for railfence
        #####
        # rails = []
        # for i in range(self.length):
        #     rails.append([])
        # for i, c in enumerate(s):
        #     rails[i % self.length].append(c)
        # return ''.join(''.join(r) for r in rails)

        # groups = grouper(s, self.length, fillvalue=NULLCHAR)
        # return roundrobin(*groups)

    def _decode(self, s):
        # rails = OrderedDict()
        # keys = range(self.key)
        # z = utils.zigzag(keys)
        # rail_counts = Counter(itertools.islice(z, len(s)))
        # print(rail_counts)

        # could easily start at zero, again [TODO] to test use of counter
        # and dict as being robust and superior over array/list
        rails_in_order = list(range(1, self.key+1))

        z = utils.zigzag(rails_in_order)

        #### using str here to ensure that OrderedCounter below actually works
        # as opposed to typical Counter, which will preserve order of int keys
        ## [TODO] remove str() before final version
        rail_slices = list(str(n) for n in itertools.islice(z, len(s)))
        # rail_slices = list(itertools.islice(z, len(s)))
        # z = utils.zigzag(rails_in_order)
        # zippy = (list(zip(z, s)))
        #### c is not guaranteed to store keys in order

        period = 2 * (self.key - 1)
        one_period_of_zigzags = rail_slices[:period]

        #### combine with OrderedDict
        # c = Counter(rail_slices)  # how many characters are in each row?
        d = OrderedCounter(rail_slices)
        # print(d)
        # rail_lengths = { rail: rail_len for rail, rail_len in d.items() }
        # rail_counts = [ (rail,c[rail]) for rail in rails_in_order]
        # rail_counts2 = [(rail, crail) for rail,crail in d.items()]
        # print('---')
        # print(rail_counts)
        # print(rail_counts2)
        # print('===')

        t = iter(s)
        # rails = [iter(take(c[rail], t)) for rail in rails_in_order]
        fence = {k: iter(take(v, t)) for k, v in d.items()} # rail: count
        # rail_iters = (rails[rail] for rail in rail_slices)
        rail_iters2 = (fence[rail] for rail in one_period_of_zigzags)

        # out = map(next, rail_iters)
        # out = [next(rail_iter) for rail_iter in rail_iters]
        out = utils.roundrobin(*rail_iters2)

        # x = [take(c[rail], t) for rail in rails_in_order]
        # y = itertools.tee(t, self.key)
        # [take(c[rail], m) for m in r
        # ends = itertools.accumulate(c[rail] for rail in rails_in_order)

        # rails = { rail: iter(list(itertools.islice(t, c[rail])))
        #           for rail in rails_in_order }
        # rails = { rail: iter(x[rail]) for rail in rails_in_order }
        # rails = [iter(x[rail]) for rail in rails_in_order]
        # rails = { rail: iter( list( next(t) for __ in range(count) ))
        #               for rail, count in c.items() }

        # out = map(next, (rails[rail] for rail in rail_slices))
        ### use roundrobin?

        # out = map(next, map(rails.__getitem__, rail_slices))
        # out = [next(rail_contents) for rail_contents in
        #     (rails[rail] for rail in rail_slices)]

        return ''.join(out)
