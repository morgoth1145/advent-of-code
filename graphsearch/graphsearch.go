package graphsearch

import "sort"

// A graph that satisfies graphsearch.Interface can be searched by the
// routines in this package. The methods require that the nodes in the
// graph have unique integer keys
type Interface interface {
	Neighbors(node int) []GraphLink
}

// GraphLink represents a connection in the graph
type GraphLink struct {
	Node     int
	Distance int
}

// AllReachable returns all the connections (direct and indirect)
// from a starting node
func AllReachable(graph Interface, start int) []GraphLink {
	foundLinks := []GraphLink{}
	seen := map[int]bool{}
	queue := []GraphLink{GraphLink{start, 0}}
	for len(queue) > 0 {
		currentStep := queue[0]
		queue = queue[1:]
		if seen[currentStep.Node] {
			continue
		}
		seen[currentStep.Node] = true

		if currentStep.Node != start {
			foundLinks = append(foundLinks, currentStep)
		}

		for _, link := range graph.Neighbors(currentStep.Node) {
			queue = append(queue, GraphLink{link.Node, currentStep.Distance + link.Distance})
		}

		// TODO: Priority queue
		sort.Slice(queue, func(i, j int) bool {
			return queue[i].Distance < queue[j].Distance
		})
	}
	return foundLinks
}
