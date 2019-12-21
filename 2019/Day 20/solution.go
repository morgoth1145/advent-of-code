package main

import (
	"advent-of-code/aochelpers"
	"advent-of-code/graphsearch"
	"sort"
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

type mazeGraph struct {
	m         maze
	nodeToPos map[int]vector2D
	posToNode map[vector2D]int
}

func (mg *mazeGraph) Neighbors(node int) []graphsearch.GraphLink {
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
		mg := mazeGraph{
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

func solve(maze map[string][]graphLink, start string, end string) int {
	seen := map[string]bool{}
	queue := []graphLink{graphLink{start, 0}}
	for len(queue) > 0 {
		item := queue[0]
		if item.dest == end {
			return item.dist
		}
		queue = queue[1:]
		tile := item.dest
		if seen[tile] {
			continue
		}
		seen[tile] = true
		for _, link := range maze[tile] {
			queue = append(queue, graphLink{link.dest, item.dist + link.dist})
		}
		sort.Slice(queue, func(i, j int) bool {
			return queue[i].dist < queue[j].dist
		})
	}
	panic("Did not finish the maze!")
}

func part1(input string) {
	maze := parseToGraph(input)
	println("The answer to part one is " + strconv.Itoa(solve(maze, "AA", "ZZ")))
}

type solveRecursiveStep struct {
	layer int
	dest  string
	dist  int
}

func solve2(maze map[string][]graphLink, start string, end string) int {
	seen := map[string]bool{}
	getKey := func(layer int, label string) string {
		return strconv.Itoa(layer) + ":" + label
	}
	queue := []solveRecursiveStep{solveRecursiveStep{0, start, 0}}
	for len(queue) > 0 {
		item := queue[0]
		queue = queue[1:]
		layer := item.layer
		tile := item.dest
		if layer == 0 && tile == end {
			return item.dist
		}
		key := getKey(layer, tile)
		if seen[key] {
			continue
		}
		seen[key] = true
		for _, link := range maze[tile] {
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
			if tile[:2] == link.dest[:2] {
				if tile[2:] == "In" {
					newLayer++
				} else {
					newLayer--
				}
			}
			if newLayer < 0 {
				continue // This is invalid
			}
			queue = append(queue, solveRecursiveStep{newLayer, link.dest, item.dist + link.dist})
		}
		sort.Slice(queue, func(i, j int) bool {
			return queue[i].dist < queue[j].dist
		})
	}
	panic("Did not finish the maze!")
}

func part2(input string) {
	maze := parseToGraph(input)
	println("The answer to part two is " + strconv.Itoa(solve2(maze, "AA", "ZZ")))
}
