
#def scramble(seq, mapping):
#  for m in mapping:
#    yield seq[m % len(seq)]


# def shares_prime_factors(x, y):
#     c = gcd(x, y)
#     z = y // c
#     while True:
#         if z == 1:
#             return True
#         c = gcd(x, z)
#         if c == 1:
#             return False
#         z = z // c

# def reduce_coprime_pair(a, b):
#     c = math.gcd(a, b)
#     return (a // c, b // c)

def coprime_factors(x, y):
    """ does X have all the prime factors of Y?

    Parameters
    ----------
    x : int
        A number to check for shared prime factors.
    y : int
        A number whose prime factors must be in `x`.

    Notes
    -----
    is there a formal name for this process?

    Given two positive integers A and B:

    1. Get GCD of A and B, C
    2. If C == 1, numbers are coprime.  Return `False`.
    3. Divide B by C.
    4. If C == B, A is divisible at least once by all prime factors of
       (original) B.  Return `True`.
    5. Return to step 1, repeating as many times as necessary (may be none, may
       be several or more).

    """
    if x == 0 or y == 0:
        raise ValueError('Neither `x` nor `y` may be zero.')

        
        # c = math.gcd(x_, y_)
        # print('x,y|c => {}, {} '.format(x_, y_))
        # if c != 1:  # run until x and y (both mutated below) are coprime
        #     return inner(c, y_ // c)
        # return y_

        ## THIS ONE APPEARS PRETTY SOLID...
        # while x_ != 1:  # run until x and y (both mutated below) are coprime
        #     x_ = math.gcd(x_, y_)
        #     y_ //= x_
        #     print('x,y|c => {}, {} '.format(x_, y_))
        # return y_

    final_x = regular(y, x)
    final_y = regular(x, y)

    print('({}, {}) => ({}, {})'.format(x, y, final_x, final_y))  # could we return this instead of boolean?
    # if so, what does Y represent?
    return y == 1  # if y == 1, y prime factors divide x; otherwise, coprime

    while True:  # this matches Stack Exchange post at http://math.stackexchange.com/questions/1275848/one-number-divisible-by-all-prime-factors-of-another
        c = math.gcd(x, y)
        x = c
        y //= c

        print('x,y|c => {}, {} | {}'.format(x, y, c))

        if c == 1:
            # if y == 1, y divides into x; otherwise, x and y are coprime
            return y == 1
        # return contains_prime_factors_of(c, y // c)  # if no `while` loop

    while not coprime(x, y):  # or `while math.gcd(x, y) != 1:`
        print('{},{}|{}'.format(x, y, math.gcd(x,y)))
        # print(math.gcd(x,y))
        # print(lcm(x,y))
        y //= math.gcd(x, y)

        # y = y * lcm(x, y)

        # y = lcm(x, y) // x
        if y == 1:
            return True
    return False

    # while not coprime(x, y):  # or `while math.gcd(x, y) != 1:`
    #     if x % y == 0:  # or `if math.gcd(x, y) == y:`
    #         return True
    #     else:
    #         y //= math.gcd(x, y)
    # return False

    # if result is divisible by somehow reduced-to-unique prime factors number
    # (e.g., 2*2*3*3*5 => x % (2*3*5) == 0), we can return True
    while True:
        c = math.gcd(x, y)
        print('x,y|c => {}, {} | {}'.format(x, y, c))
        if c == 1:  # coprime
            return False
        elif c == y:  # or if x % y == 0
            return True
        else:
            y //= c

    # while True:
    #     c = y // math.gcd(x, y)
    #     print('x,y|c => {}, {} | {}'.format(x, y, c))
    #     if c == y:  # coprime
    #         return False
    #     elif c == 1:  # or if x % y == 0
    #         return True
    #     else:
    #         y //= c

        if gcd(x, y) == 1:
            return False # coprime
        elif gcd(x, y) == y:
            return True  # x divisible by all prime factors of y
        else:
            y = y // gcd(x, y)


def tester(x,y):
    while y != 1:  # loops infinitely... heh
        if x % y == 0:
            return True
        else:
            y //= math.gcd(x, y)
    return False


    while True:
        c = math.gcd(x, y)
        if c == 1:
            return False
        elif x % y == 0:
            return True
        else:
            y //= c


def tester(x,y):
    while x % y != 0:
        c = math.gcd(x, y)
        if c == 1:
            return False
        else:
            y //= math.gcd(x, y)
    return True
        # if x % y == 0:  # X divisible by Y, thus Y is GCF of X and Y
        #     return True
    # c = math.gcd(x, y)
    # if c == y:
    #     return True


    # print('{}, {}'.format(x, y))

    # c = gcd(x, y)
    # y //= c
    # while True:
    #     print('x, y, gcd = {}, {}, {}'.format(x, y, y*gcd(x, y)))
    #     if y == 1:  # for first step, y //= gcd(x, y) == y indicates that x is multiple of y
    #         return True
    #     c = gcd(x, y)
    #     if c == 1:  # x and y (reduced) are coprime
    #         return False
    #     y //= c

    # while not coprime(x, y):
    #     print('x, y, gcd = {}, {}, {}'.format(x, y, gcd(x, y)))
    #     if x % y == 0:  # if X is divisible by Y, then X is divisible by all prime factors of Y
    #         return True
    #     y //= gcd(x, y)
    # return False

        # if gcd(x, y) == y:  # for first step, y //= gcd(x, y) == y indicates that x is multiple of y
        #     return True
        # 24,8=>8
        # 24,6=>6
        # 24,12
        # ***if x is evenly divisible by y, does that make y the GCD of x and y

        # 14 and 7==> 7 is GCD of 14 and 7
        # 14 and 2==> 2 is GCD of 14 and 2
        # 12 and 8==> 4 is GCD of 12 and 8
    # while True:
    #     print('going through')
    #     if x % y == 0:  # if X is divisible by Y, then X is divisible by all prime factors of Y
    #         return True
    #     # c = gcd(x, y)
    #     if gcd(x, y) == 1:  # x and y (reduced) are coprime
    #         return False
    #     y //= gcd(x, y)


    # while True:
    #     c = gcd(x, y)
    #     if c == 1:  # x and y (reduced) are coprime
    #         return False
    #     y //= c
    #     if y == 1:  # for first step, y //= gcd(x, y) == y indicates that x is multiple of y
    #         return True

    # c = gcd(x, y)
    # y //= c
    # while True:
    #     if y == 1:  # for first step, y //= gcd(x, y) == y indicates that x is multiple of y
    #         return True
    #     c = gcd(x, y)
    #     if c == 1:  # x and y (reduced) are coprime
    #         return False
    #     y //= c


# def finite_ap(start, count, interval):
#     """ Generate a finite arithmetic progression.

#     Parameters
#     ----------
#     start : int
#         The initial term of the sequence.
#     count : int
#         The length of the sequence to generate.
#     interval : int
#         The common difference of the sequence.

#     Returns
#     -------
#     out : generator
#         The resulting sequence as a generator.

#     Notes
#     -----
#     This is essentially just a loose cover for the Python `range` builtin.

#     """
#     return range(start, count * interval + start, interval)


