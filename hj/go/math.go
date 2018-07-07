package main

import (
	"fmt"
	"math/big"
)

// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
func xgcd(b, a int) (int, int, int) {
	x0, x1, y0, y1 := 1, 0, 0, 1
	for a != 0 {
		q := b / a
		b, a = a, b%a
		x0, x1 = x1, x0-q*x1
		y0, y1 = y1, y0-q*y1
	}
	return b, x0, y0
}

// adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Iterative_algorithm_3
// return (g, x, y) a*x + b*y = gcd(x, y)
func egcd(a, b int) (int, int, int) {
	if a == 0 {
		return b, 0, 1
	} else {
		g, x, y := egcd(b%a, a)
		return g, y - (b/a)*x, x
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
/*func Modulus(a, b int) int {
	return ((a % b) + b) % b
}*/

// Divides tests if a number `b` evenly divides `a`.
func Divides(a, b *big.Int) bool {
	return new(big.Int).Mod(a, b).Int64() == 0
}

// Coprime tests if two numbers `a` and `b` are relatively prime.
// The order of the parameters does not matter.
func Coprime(a, b *big.Int) bool {
	gcd := new(big.Int).GCD(nil, nil, a, b)
	return gcd.Int64() == 1
}

func makeLCG2(m, a, c, seed int) (func() int, bool) {
	hull_dobell := true

	if m <= 0 {
		panic("modulus must be greater than zero")
	}
	if a <= 0 {
		panic("multiplier must be greater than zero")
	}
	if c < 0 {
		panic("increment must be greater than or equal to zero")
	}
	if seed < 0 {
		panic("start value must be greater than or equal to zero")
	}

	newseed := seed % m
	var prevseed int
	out := func() int {
		// seed = (newseed * a + c) % m
		// prevseed.Set(newseed)
		prevseed = newseed
		newseed = (newseed*a + c) % m
		// newseed.Mul(newseed, a).Add(newseed, c).Mod(newseed, m)
		return prevseed
	}

	// A_MINUS_ONE := a - 1
	// DIVISIBLE_BY_FOUR := func(a int) bool { return a%4 == 0 }
	switch {
	// case !Coprime(m, c):
	// 	fmt.Println("Multiplier and increment should be coprime:", m, c)
	// 	hull_dobell = false
	// case !Regular(m, A_MINUS_ONE):
	// 	fmt.Println("Prime factors of `m` should also divide `a - 1`")
	// 	hull_dobell = false
	case m%4 == 0 && (a-1)%4 != 0:
		fmt.Println("If 4 divides `m`, 4 should divide `a - 1`")
		hull_dobell = false
	}

	return out, hull_dobell
}

// TODO: document
// TODO: TESTS
// TODO: USE GOROUTINES and channel and then emulate yield in inner func???
func makeLCG(m, a, c, seed *big.Int) (func() *big.Int, bool) {
	hull_dobell := true

	A_MINUS_ONE := new(big.Int).Sub(a, big.NewInt(1))
	DIVISIBLE_BY_FOUR := func(a *big.Int) bool { return Divides(a, big.NewInt(4)) }
	switch {
	case !Coprime(m, c):
		fmt.Println("Multiplier and increment should be coprime:", m, c)
		hull_dobell = false
	case !Regular(m, A_MINUS_ONE):
		fmt.Println("Prime factors of `m` should also divide `a - 1`")
		hull_dobell = false
	case DIVISIBLE_BY_FOUR(m) && !DIVISIBLE_BY_FOUR(A_MINUS_ONE):
		fmt.Println("If 4 divides `m`, 4 should divide `a - 1`")
		hull_dobell = false
	}

	newseed := new(big.Int).Mod(seed, m)
	prevseed := new(big.Int)
	return func() *big.Int {
		// seed = (newseed * a + c) % m
		prevseed.Set(newseed)
		newseed.Mul(newseed, a).Add(newseed, c).Mod(newseed, m)
		return prevseed
	}, hull_dobell
}

// just return true if either a or b is zero?
func Regular(a, b *big.Int) bool {
	if a.Int64() == 0 {
		fmt.Println("Parameter `a` must be nonzero.")
		//raise ValueError('')
	}
	if b.Int64() == 0 {
		return true
	}

	a_, b_ := new(big.Int).Set(a), new(big.Int).Set(b)
	for b_.Int64() != 1 {
		b_.GCD(nil, nil, b_, a_)
		a_.Div(a_, b_)
	}
	return a_.Int64() == 1
}
