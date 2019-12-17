package helpers

// PermuteInts generates the permutations of an integer list
func PermuteInts(values ...int) chan []int {
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

// ReverseStrings returns the list of strings in reverse order
func ReverseStrings(list []string) []string {
	out := append([]string{}, list...)
	for i, j := 0, len(out)-1; i < j; i, j = i+1, j-1 {
		out[i], out[j] = out[j], out[i]
	}
	return out
}

// ReverseInts returns the list of ints in reverse order
func ReverseInts(list []int) []int {
	out := append([]int{}, list...)
	for i, j := 0, len(out)-1; i < j; i, j = i+1, j-1 {
		out[i], out[j] = out[j], out[i]
	}
	return out
}

// PartialSumsInt calculates the partial sums of a list
func PartialSumsInt(list []int) []int {
	out := []int{}
	tot := 0
	for _, v := range list {
		tot += v
		out = append(out, tot)
	}
	return out
}
