package helpers

// Abs returns the absolute value of an int
func Abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

// GCD calculates the greatest common denominator of two integers
func GCD(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// GCD64 calculates the greatest common denominator of two integers
func GCD64(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// LCM calculates the least common multiple of a series of integers
func LCM(input ...int) int {
	out := 1
	for _, v := range input {
		out = out / GCD(out, v) * v
	}
	return out
}

// LCM64 calculates the least common multiple of a series of integers
func LCM64(input ...int64) int64 {
	out := int64(1)
	for _, v := range input {
		out = out / GCD64(out, v) * v
	}
	return out
}
