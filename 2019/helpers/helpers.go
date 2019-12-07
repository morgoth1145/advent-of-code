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
