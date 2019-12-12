package helpers

// Abs returns the absolute value of an int
func Abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

// IntPermutations generates the permutations of an integer list
func IntPermutations(values ...int) chan []int {
	out := make(chan []int)
	var impl func(int)
	impl = func(idx int) {
		if idx == len(values) {
			out <- append([]int{}, values...)
			return
		}
		impl(idx + 1)
		for j := idx + 1; j < len(values); j++ {
			values[idx], values[j] = values[j], values[idx]
			impl(idx + 1)
			values[idx], values[j] = values[j], values[idx]
		}
		if 0 == idx {
			close(out)
		}
	}
	go impl(0)
	return out
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
