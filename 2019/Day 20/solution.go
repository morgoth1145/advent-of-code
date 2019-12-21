package main

import (
	"advent-of-code/aochelpers"
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

func surroundingTiles(pos vector2D) []vector2D {
	return []vector2D{
		vector2D{pos.x - 1, pos.y},
		vector2D{pos.x + 1, pos.y},
		vector2D{pos.x, pos.y - 1},
		vector2D{pos.x, pos.y + 1},
	}
}

func parseToGraph(input string) map[string][]graphLink {
	maze := map[vector2D]rune{}
	for y, line := range strings.Split(input, "\n") {
		for x, c := range line {
			if c == ' ' {
				continue
			}
			maze[vector2D{x, y}] = c
		}
	}
	labels := map[string]vector2D{}
	posToLabel := map[vector2D]string{}
	for pos, c := range maze {
		if c == '.' {
			for _, n := range surroundingTiles(pos) {
				t := maze[n]
				if t != '.' && t != '#' {
					// It's a marker!
					t2 := maze[vector2D{n.x*2 - pos.x, n.y*2 - pos.y}]
					label := string(t) + string(t2)
					if n.x < pos.x || n.y < pos.y {
						// Marker is reversed
						label = string(t2) + string(t)
					}
					{
						_, nameTaken := labels[label]
						if nameTaken {
							label += "2"
						}
					}
					labels[label] = pos
					posToLabel[pos] = label
				}
			}
			continue
		}
	}

	out := map[string][]graphLink{}
	for label, startPos := range labels {
		links := []graphLink{}
		seen := map[vector2D]bool{}
		steps := -1
		queue := []vector2D{startPos}
		for len(queue) > 0 {
			steps++
			newQueue := []vector2D{}
			for _, pos := range queue {
				if seen[pos] {
					continue
				}
				seen[pos] = true
				cur := maze[pos]
				if cur == '#' {
					continue
				}
				if cur == '.' || pos == startPos {
					for _, n := range surroundingTiles(pos) {
						newQueue = append(newQueue, n)
					}
				}
				if pos == startPos {
					continue
				}
				foundLabel, hasLabel := posToLabel[pos]
				if hasLabel {
					links = append(links, graphLink{foundLabel, steps})
				}
			}
			queue = newQueue
		}
		out[label] = links
	}

	for label := range labels {
		if label == "AA" || label == "ZZ" {
			continue
		}
		otherLabel := label[:2]
		if label[2:] == "" {
			otherLabel += "2"
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

func part2(input string) {
}
