package channeltypes

// List makes a channel that just outputs the requested list
func List(items ...int64) <-chan int64 {
	out := make(chan int64, len(items))
	for _, v := range items {
		out <- v
	}
	close(out)
	return out
}

// Chain makes a channel that pulls from each input channel in sequence
func Chain(inputs ...<-chan int64) <-chan int64 {
	out := make(chan int64, 1)
	impl := func() {
		for _, c := range inputs {
			for v := range c {
				out <- v
			}
		}
		close(out)
	}
	go impl()
	return out
}
