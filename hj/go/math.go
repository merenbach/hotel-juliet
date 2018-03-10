package main

// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
func xgcd(b, a int) (int, int, int) {
    x0, x1, y0, y1 := 1, 0, 0, 1
    for a != 0 {
        q := b / a
        b, a = a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    }
    return  b, x0, y0
}
// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
// return (g, x, y) a*x + b*y = gcd(x, y)
func egcd(a, b int) (int, int, int) {
    if a == 0 {
        return b, 0, 1
    } else {
        g, x, y := egcd(b % a, a)
        return g, y - (b / a) * x, x
    }
}
// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
// x = mulinv(b) mod n, (x * b) % n == 1
func mulinv(b, n int) int {
	g, x, _ := egcd(b, n)
	if g == 1 {
		return x % n
	}
	return -1
}

// Modulus returns the remainder of a Euclidean division operation.
// This works around https://github.com/golang/go/issues/448
func Modulus(a, b int) int {
	return ((a % b) + b) % b
}

/*

func coprime(a, b int) ?
    """ Determine whether two integers are relatively prime.

    Parameters
    ----------
    a : int
        An integer.
    b : int
        An integer.

    Returns
    -------
    out : bool
        `True` if `a` and `b` share no prime factors, `False` otherwise.

    Notes
    -----
    The order of the parameters does not matter.

    """
    return math.gcd(a, b) == 1
}


func LCG(m, a, c, seed int, hull_dobell bool):
    """ Configure a linear congruential generator.

    Parameters
    ----------
    m : int
        The modulus.
    a : int
        The multiplier.
    c : int
        The increment of the sequence.
    seed : int
        The initial term (seed or start value) for the sequence.
    hull_dobell : bool, optional
        `True` to apply requirements of Hull-Dobell Theorem, `False` otherwise.
        This ensures that the generator has a full period for all seed values.
        Overriding this may result in a less effective PRNG.  Default `True`.

    Yields
    ------
    out : int
        The resulting infinite sequence as a generator.

    Notes
    -----
    With a multiplier of `1`, this becomes an effective generator for the
    ciphertext alphabet used in the affine cipher.

    [TODO] needs more input validation

    [TODO] unit tests very much required

    """
    // if m <= 0:
    //     raise ValueError('Constraint `0 < m` not satisfied.')
    // if m <= a or a <= 0:
    //     raise ValueError('Constraint `0 < a < m` not satisfied.')
    // if m <= c or c < 0:
    //     raise ValueError('Constraint `0 <= c < m` not satisfied.')
    // if m <= seed or seed < 0:
    //     raise ValueError('Constraint `0 <= seed < m` not satisfied.')

    // if not all([ (0 < m), (0 < a < m), (0 <= c < m), (0 <= seed < m) ]):
    //     raise ValueError('Constraints not met')

    if hull_dobell {
        if not coprime(m, c):
            raise ValueError('Multiplier and increment must be coprime.')
        if not regular(m, a - 1):
            raise ValueError('Prime factors of `m` must also divide `a - 1`.')
        if divisible(m, 4) and not divisible(a - 1, 4):
            raise ValueError('If 4 divides `m`, 4 must divide `a - 1`.')
    }

    while True:
        yield seed
        seed = (seed * a + c) % m
*/
