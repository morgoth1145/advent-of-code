package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"advent-of-code/helpers"
	"runtime"
	"strconv"
	"strings"
	"sync"
)

func main() {
	input := aochelpers.GetInput(2019, 15)
	part1(input)
	part2(input)
}

type vector2D struct {
	x int
	y int
}

func surroundingTiles(pos vector2D) []vector2D {
	return []vector2D{
		vector2D{pos.x - 1, pos.y},
		vector2D{pos.x + 1, pos.y},
		vector2D{pos.x, pos.y - 1},
		vector2D{pos.x, pos.y + 1},
	}
}

func getBestExploringPath(tiles map[vector2D]int, pos vector2D) []vector2D {
	seen := map[vector2D]bool{}
	queue := [][]vector2D{[]vector2D{pos}}
	for {
		current := queue[0]
		queue = queue[1:]
		pos := current[len(current)-1]
		seen[pos] = true

		for _, surroundingPos := range surroundingTiles(pos) {
			t, known := tiles[surroundingPos]
			if !known {
				// This is exploration!
				return append(current, surroundingPos)
			}
			_, known = seen[surroundingPos]
			if !known && t != 0 {
				queue = append(queue, append(append([]vector2D{}, current...), surroundingPos))
			}
		}
	}
}

func getBoundingBox(tiles map[vector2D]int) (vector2D, vector2D) {
	min, max := vector2D{0, 0}, vector2D{0, 0}
	for p := range tiles {
		if p.x < min.x {
			min.x = p.x
		} else if p.x > max.x {
			max.x = p.x
		}
		if p.y < min.y {
			min.y = p.y
		} else if p.y > max.y {
			max.y = p.y
		}
	}
	return min, max
}

func renderTiles(tiles map[vector2D]int) {
	min, max := getBoundingBox(tiles)
	println(strings.Repeat("-", max.x-min.x+1))
	for y := max.y; y >= min.y; y-- {
		line := ""
		for x := min.x; x <= max.x; x++ {
			tile, known := tiles[vector2D{x, y}]
			if !known {
				line += "?"
				continue
			}
			switch tile {
			case 0: // Wall
				line += "\u2588"
			case 1: // Open
				line += " "
			case 2: // System
				line += "O"
			}
		}
		println(line)
	}
	println(strings.Repeat("-", max.x-min.x+1))
}

func exploreMaze(input string) map[vector2D]int {
	pos := vector2D{0, 0}
	tiles := map[vector2D]int{pos: 1}
	unknownTiles := map[vector2D]bool{
		vector2D{1, 0}:  true,
		vector2D{-1, 0}: true,
		vector2D{0, 1}:  true,
		vector2D{0, -1}: true,
	}
	currentPath := getBestExploringPath(tiles, pos)[1:]

	m := new(sync.Mutex)
	directionFunc := func() int64 {
		m.Lock() // Unlocked by reading goroutine
		if 0 == len(currentPath) {
			runtime.Goexit() // Kill the program goroutine.
		}
		targetPos := currentPath[0]
		if pos.x < targetPos.x {
			return 4 // East
		} else if pos.x > targetPos.x {
			return 3 // West
		}
		if pos.y < targetPos.y {
			return 1 // North
		} else if pos.y > targetPos.y {
			return 2 // South
		}
		panic("I don't know where to go!")
	}
	statusChan := intcode.Parse(input).AsyncRun(directionFunc)
	for len(unknownTiles) > 0 {
		// Unlocked
		status := <-statusChan

		// Locked (an input is required prior to each output)
		targetPos := currentPath[0]
		currentPath = currentPath[1:]
		tiles[targetPos] = int(status)
		if status != 0 {
			pos = targetPos
			for _, surroundingPos := range surroundingTiles(pos) {
				_, known := tiles[surroundingPos]
				if !known {
					unknownTiles[surroundingPos] = true
				}
			}
		}
		_, learnedTile := unknownTiles[targetPos]
		if learnedTile {
			// renderTiles(tiles)
			delete(unknownTiles, targetPos)

			if 0 != len(unknownTiles) {
				currentPath = getBestExploringPath(tiles, pos)[1:]
			}
		}
		m.Unlock() // Status processed
	}
	return tiles
}

func convertToGraph(tiles map[vector2D]int) (map[int][]int, int, int) {
	nextID := 0
	vecToID := map[vector2D]int{}
	getVectorID := func(v vector2D) int {
		id, present := vecToID[v]
		if present {
			return id
		}
		id = nextID
		nextID++
		vecToID[v] = id
		return id
	}
	var system vector2D
	graph := map[int][]int{}
	for v, t := range tiles {
		if t == 0 {
			continue // Wall
		}
		if t == 2 {
			system = v
		}
		id := getVectorID(v)
		neighbors := []int{}
		for _, neighbor := range surroundingTiles(v) {
			if tiles[neighbor] != 0 {
				neighbors = append(neighbors, getVectorID(neighbor))
			}
		}
		graph[id] = neighbors
	}
	return graph, vecToID[vector2D{0, 0}], vecToID[system]
}

func part1(input string) {
	graph, start, system := convertToGraph(exploreMaze(input))
	path := helpers.ShortestIntPath(graph, start, system)
	println("The answer to part one is " + strconv.Itoa(len(path)-1))
}

func part2(input string) {
}
