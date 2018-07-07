package main

import (
	"fmt"
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

// abs returns the absolute value of an integer.
func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

// gcd returns the greatest common divisor for the provided parameters.
func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return abs(a)
}

// Coprime tests if two numbers `a` and `b` are relatively prime.
// The order of the parameters does not matter.
func Coprime(a, b int) bool {
	return gcd(a, b) == 1
}

// type LCG struct {
// 	m    int
// 	a    int
// 	c    int
// 	seed int
// }

// func NewLCG() *LCG {
// 	lcg := LCG{}
// 	return &lcg
// }

func makeLCG2(m, a, c, seed int) (func() int, bool) {
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

	hull_dobell := true

	switch {
	case !Coprime(m, c):
		fmt.Println("Multiplier and increment should be coprime:", m, c)
		hull_dobell = false
	case !Regular(m, a-1):
		fmt.Println("Prime factors of `m` should also divide `a - 1`")
		hull_dobell = false
	case m%4 == 0 && (a-1)%4 != 0:
		fmt.Println("If 4 divides `m`, 4 should divide `a - 1`")
		hull_dobell = false
	}

	return out, hull_dobell
}

// Regular tests if all prime factors of `a` also divide `b`.
// Note that the order of the parameters is important, as `b` may have additional prime factors.
// just return true if either a or b is zero?
func Regular(a, b int) bool {
	if a == 0 {
		fmt.Println("Parameter `a` must be nonzero.")
		//raise ValueError('')
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
