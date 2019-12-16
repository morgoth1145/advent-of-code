package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"advent-of-code/helpers"
	"strconv"
	"strings"
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
	tiles := map[vector2D]int{vector2D{0, 0}: 1}

	moveChan := make(chan int64, 1)
	moveChan <- 1 // North
	positionStack := []vector2D{vector2D{0, 0}, vector2D{0, 1}}

	statusChan := intcode.Parse(input).AsyncRun(intcode.InputChannelFunction(moveChan))
	for status := range statusChan {
		pos := positionStack[len(positionStack)-1]
		if _, known := tiles[pos]; !known {
			tiles[pos] = int(status)
			// renderTiles(tiles)
		}
		if status == 0 {
			// We hit a wall and didn't move
			positionStack = positionStack[:len(positionStack)-1]
			pos = positionStack[len(positionStack)-1]
		}
		advancementFound := false
		for _, n := range surroundingTiles(pos) {
			if _, known := tiles[n]; !known {
				positionStack = append(positionStack, n)
				advancementFound = true
				break
			}
		}
		if !advancementFound {
			// We need to backtrack
			positionStack = positionStack[:len(positionStack)-1]
			if 0 == len(positionStack) {
				// We've explored everything! Time to exit
				close(moveChan)
				continue
			}
		}
		nextPos := positionStack[len(positionStack)-1]
		if pos.y < nextPos.y {
			moveChan <- 1 // North
		} else if pos.y > nextPos.y {
			moveChan <- 2 // South
		} else if pos.x > nextPos.x {
			moveChan <- 3 // West
		} else if pos.x < nextPos.x {
			moveChan <- 4 // East
		} else {
			panic("I don't know where to go!")
		}
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
	graph, _, system := convertToGraph(exploreMaze(input))
	println("The answer to part two is " + strconv.Itoa(helpers.LongestIntPathLength(graph, system)))
}
