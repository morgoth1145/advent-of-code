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
