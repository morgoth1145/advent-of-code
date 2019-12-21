package main

import (
	"advent-of-code/aochelpers"
	"advent-of-code/graphsearch"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 20)
	part1(input)
	part2(input)
}

type vector2D struct {
	x int
	y int
}

type graphLink struct {
	dest string
	dist int
}

type maze struct {
	maze       map[vector2D]rune
	labels     map[string]vector2D
	posToLabel map[vector2D]string
}

func makeMaze() maze {
	return maze{
		map[vector2D]rune{},
		map[string]vector2D{},
		map[vector2D]string{},
	}
}

func surroundingTiles(pos vector2D) []vector2D {
	return []vector2D{
		vector2D{pos.x - 1, pos.y},
		vector2D{pos.x + 1, pos.y},
		vector2D{pos.x, pos.y - 1},
		vector2D{pos.x, pos.y + 1},
	}
}

func parseMaze(input string) maze {
	m := makeMaze()
	maxX, maxY := 0, 0
	for y, line := range strings.Split(input, "\n") {
		if y > maxY {
			maxY = y
		}
		for x, c := range line {
			if x > maxX {
				maxX = x
			}
			if c == ' ' {
				continue
			}
			m.maze[vector2D{x, y}] = c
		}
	}

	for pos, c := range m.maze {
		if c == '.' {
			for _, n := range surroundingTiles(pos) {
				t := m.maze[n]
				if t != '.' && t != '#' {
					// It's a marker!
					t2 := m.maze[vector2D{n.x*2 - pos.x, n.y*2 - pos.y}]
					label := string(t) + string(t2)
					if n.x < pos.x || n.y < pos.y {
						// Marker is reversed
						label = string(t2) + string(t)
					}
					if label != "AA" && label != "ZZ" {
						if n.x == 1 || n.y == 1 || n.x == maxX-1 || n.y == maxY-1 {
							// Outer
							label += "Out"
						} else {
							// Inner
							label += "In"
						}
					}
					m.labels[label] = pos
					m.posToLabel[pos] = label
				}
			}
			continue
		}
	}
	return m
}

type mazeGraphAdaptor struct {
	m         maze
	nodeToPos map[int]vector2D
	posToNode map[vector2D]int
}

func (mg *mazeGraphAdaptor) Neighbors(node int) []graphsearch.GraphLink {
	out := []graphsearch.GraphLink{}
	pos := mg.nodeToPos[node]
	for _, n := range surroundingTiles(pos) {
		neighborNode, ok := mg.posToNode[n]
		if !ok {
			if mg.m.maze[n] != '.' {
				continue
			}
			neighborNode = len(mg.nodeToPos)
			mg.nodeToPos[neighborNode] = n
			mg.posToNode[n] = neighborNode
		}
		out = append(out, graphsearch.GraphLink{Node: neighborNode, Distance: 1})
	}
	return out
}

func parseToGraph(input string) map[string][]graphLink {
	m := parseMaze(input)

	out := map[string][]graphLink{}
	for label, startPos := range m.labels {
		mg := mazeGraphAdaptor{
			m,
			map[int]vector2D{},
			map[vector2D]int{},
		}
		mg.nodeToPos[0] = startPos
		mg.posToNode[startPos] = 0
		links := []graphLink{}
		for _, n := range graphsearch.AllReachable(&mg, 0) {
			label := m.posToLabel[mg.nodeToPos[n.Node]]
			if len(label) > 0 {
				links = append(links, graphLink{label, n.Distance})
			}
		}
		out[label] = links
	}

	for label := range m.labels {
		if label == "AA" || label == "ZZ" {
			continue
		}
		baseLabel := label[:2]
		otherLabel := baseLabel
		if label[2:] == "Out" {
			otherLabel += "In"
		} else {
			otherLabel += "Out"
		}
		out[label] = append(out[label], graphLink{otherLabel, 1})
	}

	return out
}

type mazeGraph struct {
	maze        map[string][]graphLink
	nodeToLabel map[int]string
	labelToNode map[string]int
}

func (mg mazeGraph) Neighbors(node int) []graphsearch.GraphLink {
	out := []graphsearch.GraphLink{}
	label := mg.nodeToLabel[node]
	for _, link := range mg.maze[label] {
		out = append(out, graphsearch.GraphLink{Node: mg.labelToNode[link.dest], Distance: link.dist})
	}
	return out
}

func part1(input string) {
	maze := parseToGraph(input)
	nodeToLabel := map[int]string{}
	labelToNode := map[string]int{}
	for label := range maze {
		node := len(labelToNode)
		labelToNode[label] = node
		nodeToLabel[node] = label
	}
	graph := mazeGraph{maze, nodeToLabel, labelToNode}
	answer := graphsearch.DijkstraLength(graph, graph.labelToNode["AA"], graph.labelToNode["ZZ"])
	println("The answer to part one is " + strconv.Itoa(answer))
}

type mazeGraph2 struct {
	maze        map[string][]graphLink
	nodeToState map[int]string
	stateToNode map[string]int
}

func (mg *mazeGraph2) Neighbors(node int) []graphsearch.GraphLink {
	out := []graphsearch.GraphLink{}
	parts := strings.Split(mg.nodeToState[node], ":")
	layer, _ := strconv.Atoi(parts[0])
	label := parts[1]
	for _, link := range mg.maze[label] {
		if link.dest[:2] == "AA" {
			// This is never useful
			continue
		}
		if layer != 0 {
			if link.dest[:2] == "ZZ" {
				// Entrance/exit are invalid on inner layers
				continue
			}
		}
		newLayer := layer
		if label[:2] == link.dest[:2] {
			if label[2:] == "In" {
				newLayer++
			} else {
				newLayer--
			}
		}
		if newLayer < 0 {
			continue // This is invalid
		}
		linkKey := strconv.Itoa(newLayer) + ":" + link.dest
		neighborNode, ok := mg.stateToNode[linkKey]
		if !ok {
			neighborNode = len(mg.nodeToState)
			mg.nodeToState[neighborNode] = linkKey
			mg.stateToNode[linkKey] = neighborNode
		}
		out = append(out, graphsearch.GraphLink{Node: neighborNode, Distance: link.dist})
	}
	return out
}

func part2(input string) {
	maze := parseToGraph(input)
	graph := mazeGraph2{
		maze,
		map[int]string{0: "0:AA", 1: "0:AA"},
		map[string]int{"0:AA": 0, "0:ZZ": 1},
	}
	println("The answer to part two is " + strconv.Itoa(graphsearch.DijkstraLength(&graph, 0, 1)))
}
