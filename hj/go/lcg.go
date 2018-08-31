package main

import (
	"errors"
)

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
func coprime(a, b uint) bool {
	return gcd(a, b) == 1
}

// Regular tests if all prime factors of `a` also divide `b`.
// Note that the order of the parameters is important, as `b` may have additional prime factors.
// just return true if either a or b is zero?
func regular(a, b uint) bool {
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

// An LCG is a linear congruential generator, a method of generating pseudo-random numbers.
// TODO: this may be better as a simple generator function, rather than a struct.
type LCG struct {
	modulus    uint // m
	multiplier uint // a
	increment  uint // c
	seed       uint // X_0
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
		seed:       seed,
	}
}

// HullDobell tests for compliance with the Hull-Dobell theorem.
// The error parameter, if set, will contain the first-found failing constraint.
// When c != 0, this test passing means that the cycle is equal to g.multiplier.
func (g *LCG) HullDobell() (bool, error) {
	switch {
	case !coprime(g.modulus, g.increment):
		return false, errors.New("multiplier and increment should be coprime")
	case !regular(g.modulus, g.multiplier-1):
		return false, errors.New("prime factors of modulus should also divide multiplier-minus-one")
	case g.modulus%4 == 0 && (g.multiplier-1)%4 != 0:
		return false, errors.New("if 4 divides modulus, 4 should divide multiplier-minus-one")
	default:
		return true, nil
	}
}

// Iterator returns a generator function to iterate over the values of the LCG.
func (g *LCG) Iterator() func() uint {
	state := g.seed % g.modulus
	return func() uint {
		prev := state
		state = (state*g.multiplier + g.increment) % g.modulus
		return prev
	}
}
