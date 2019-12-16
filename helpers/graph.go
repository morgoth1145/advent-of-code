package helpers

// TopologicalSortStrings returns the list of strings from a graph in topological order
// The output list is sorted from leaf to root
// NOTE: THIS DOES NOT WORK FOR CYCLIC GRAPHS!
func TopologicalSortStrings(graph map[string][]string) []string {
	out := []string{}
	handled := map[string]bool{}
	var impl func(string)
	impl = func(item string) {
		{
			_, alreadyDone := handled[item]
			if alreadyDone {
				return
			}
		}
		handled[item] = true
		for _, child := range graph[item] {
			impl(child)
		}
		out = append(out, item)
	}
	for key := range graph {
		impl(key)
	}
	return out
}

// ShortestIntPath searches for and returns the shortest path from start to end in the graph
// This uses BFS
func ShortestIntPath(graph map[int][]int, start int, end int) []int {
	seen := map[int]bool{}
	queue := [][]int{[]int{start}}
	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]
		pos := current[len(current)-1]
		seen[pos] = true
		if pos == end {
			return current
		}

		for _, neighbor := range graph[pos] {
			if !seen[neighbor] {
				queue = append(queue, append(append([]int{}, current...), neighbor))
			}
		}
	}
	return nil // No path!
}

// LongestIntPathLength returns the length of the longest path from start to somewhere in the graph
func LongestIntPathLength(graph map[int][]int, start int) int {
	seen := map[int]bool{start: true}
	steps := -1
	queue := []int{start}
	for len(queue) > 0 {
		steps++
		newQueue := []int{}
		for _, pos := range queue {
			for _, n := range graph[pos] {
				_, alreadySeen := seen[n]
				if !alreadySeen {
					newQueue = append(newQueue, n)
					seen[n] = true
				}
			}
		}
		queue = newQueue
	}
	return steps
}
