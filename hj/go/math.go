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

func modulus(a, b int) int {
	// since the % is "remainder," not "modulus"...
	// work around https://github.com/golang/go/issues/448
	return ((a % b) + b) % b
}

func affine(x, a, b, m int) int {
	return modulus(a * x + b, m)
}

func invaffine(x, a, b, m int) int {
	modinv := mulinv(a, m)
	return modulus(modinv * (x - b), m)
}
