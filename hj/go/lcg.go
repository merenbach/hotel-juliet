package main

import (
	"errors"
)

// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
// func xgcd(b, a int) (int, int, int) {
// 	x0, x1, y0, y1 := 1, 0, 0, 1
// 	for a != 0 {
// 		q := b / a
// 		b, a = a, b%a
// 		x0, x1 = x1, x0-q*x1
// 		y0, y1 = y1, y0-q*y1
// 	}
// 	return b, x0, y0
// }

// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
// return (g, x, y) a*x + b*y = gcd(x, y)
// func egcd(a, b int) (int, int, int) {
// 	if a == 0 {
// 		return b, 0, 1
// 	} else {
// 		g, x, y := egcd(b%a, a)
// 		return g, y - (b/a)*x, x
// 	}
// }

// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
// x = mulinv(b) mod n, (x * b) % n == 1
// func mulinv(b, n int) int {
// 	g, x, _ := egcd(b, n)
// 	if g == 1 {
// 		return x % n
// 	}
// 	return -1
// }

// Modulus returns the remainder of a Euclidean division operation.
// This works around https://github.com/golang/go/issues/448
/*func Modulus(a, b int) int {
	return ((a % b) + b) % b
}*/

// // abs returns the absolute value of an integer.
// func abs(a int) int {
// 	if a < 0 {
// 		return -a
// 	}
// 	return a
// }

// gcd returns the greatest common divisor for the provided parameters.
func gcd(a, b uint) uint {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// Coprime tests if two numbers `a` and `b` are relatively prime.
// The order of the parameters does not matter.
func Coprime(a, b uint) bool {
	return gcd(a, b) == 1
}

type LCG struct {
	modulus    uint // m
	multiplier uint // a
	increment  uint // c
	state      uint
}

// NewLCG creates a pointer to a new LCG.
func NewLCG(m, a, c, seed uint) *LCG {
	if m == 0 {
		panic("modulus must be greater than zero")
	}
	if a == 0 {
		panic("multiplier must be greater than zero")
	}

	return &LCG{
		modulus:    m,
		multiplier: a,
		increment:  c,
		state:      seed % m,
	}
}

// HullDobell tests for compliance with the Hull-Dobell theorem.
// The error parameter, if set, will contain the first-found failing constraint.
// When c != 0, this test passing means that the cycle is equal to g.multiplier.
func (g *LCG) HullDobell() (bool, error) {
	switch {
	case !Coprime(g.modulus, g.increment):
		return false, errors.New("multiplier and increment should be coprime")
	case !Regular(g.modulus, g.multiplier-1):
		return false, errors.New("prime factors of modulus should also divide multiplier-minus-one")
	case g.modulus%4 == 0 && (g.multiplier-1)%4 != 0:
		return false, errors.New("if 4 divides modulus, 4 should divide multiplier-minus-one")
	default:
		return true, nil
	}
}

// Next returns the next value in the generator.
func (g *LCG) Next() uint {
	state := g.state
	g.state = (state*g.multiplier + g.increment) % g.modulus
	return state
}

// Regular tests if all prime factors of `a` also divide `b`.
// Note that the order of the parameters is important, as `b` may have additional prime factors.
// just return true if either a or b is zero?
func Regular(a, b uint) bool {
	if a == 0 {
		panic("Parameter `a` must be nonzero.")
	}
	if b == 0 {
		return true
	}

	for b != 1 {
		b = gcd(a, b)
		a /= b
	}
	return a == 1
}
