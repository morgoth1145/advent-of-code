package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 18)
	part1(input)
	part2(input)
}

func parseGrid(input string) [100][100]bool {
	out := [100][100]bool{}
	for x, line := range strings.Split(input, "\n") {
		for y, c := range line {
			if c == '#' {
				out[x][y] = true
			} else {
				out[x][y] = false
			}
		}
	}
	return out
}

func countNeighborsOn(grid [100][100]bool, x int, y int) int {
	count := 0
	if x > 0 {
		if y > 0 {
			if grid[x-1][y-1] {
				count++
			}
		}
		if y < 99 {
			if grid[x-1][y+1] {
				count++
			}
		}
		if grid[x-1][y] {
			count++
		}
	}
	if x < 99 {
		if y > 0 {
			if grid[x+1][y-1] {
				count++
			}
		}
		if y < 99 {
			if grid[x+1][y+1] {
				count++
			}
		}
		if grid[x+1][y] {
			count++
		}
	}
	if y > 0 {
		if grid[x][y-1] {
			count++
		}
	}
	if y < 99 {
		if grid[x][y+1] {
			count++
		}
	}
	return count
}

func iterate(grid [100][100]bool) [100][100]bool {
	newGrid := [100][100]bool{}
	for x := 0; x < 100; x++ {
		for y := 0; y < 100; y++ {
			count := countNeighborsOn(grid, x, y)
			switch count {
			case 3:
				newGrid[x][y] = true
			case 2:
				newGrid[x][y] = grid[x][y]
			default:
				newGrid[x][y] = false
			}
		}
	}
	return newGrid
}

func part1(input string) {
	grid := parseGrid(input)
	for idx := 0; idx < 100; idx++ {
		grid = iterate(grid)
	}
	count := 0
	for x := 0; x < 100; x++ {
		for y := 0; y < 100; y++ {
			if grid[x][y] {
				count++
			}
		}
	}
	println("The answer to part one is " + strconv.Itoa(count))
}

func turnOnCorners(grid [100][100]bool) [100][100]bool {
	grid[0][0] = true
	grid[99][0] = true
	grid[0][99] = true
	grid[99][99] = true
	return grid
}

func part2(input string) {
	grid := turnOnCorners(parseGrid(input))
	for idx := 0; idx < 100; idx++ {
		grid = turnOnCorners(iterate(grid))
	}
	count := 0
	for x := 0; x < 100; x++ {
		for y := 0; y < 100; y++ {
			if grid[x][y] {
				count++
			}
		}
	}
	println("The answer to part two is " + strconv.Itoa(count))
}
