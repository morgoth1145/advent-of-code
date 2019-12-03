package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 3)
	part1(input)
	part2(input)
}

type position struct {
	x int
	y int
}

func getWirePositions(wire string) map[position]int {
	out := map[position]int{}
	x, y := 0, 0
	steps := 0
	for _, part := range strings.Split(wire, ",") {
		d := part[0]
		vx, vy := 0, 0
		amount, _ := strconv.Atoi(part[1:])
		switch d {
		case 'U':
			vy = 1
		case 'D':
			vy = -1
		case 'R':
			vx = 1
		case 'L':
			vx = -1
		}
		for i := 0; i < amount; i++ {
			x += vx
			y += vy
			steps++
			pos := position{x, y}
			_, present := out[pos]
			if !present {
				out[pos] = steps
			}
		}
	}
	return out
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func part1(input string) {
	parts := strings.Split(input, "\n")
	wire1 := getWirePositions(parts[0])
	wire2 := getWirePositions(parts[1])

	best := -1
	for pos := range wire1 {
		_, present := wire2[pos]
		if present {
			dist := abs(pos.x) + abs(pos.y)
			if best == -1 || dist < best {
				best = dist
			}
		}
	}

	println("The answer to part one is " + strconv.Itoa(best))
}

func part2(input string) {
	parts := strings.Split(input, "\n")
	wire1 := getWirePositions(parts[0])
	wire2 := getWirePositions(parts[1])

	best := -1
	for pos, steps1 := range wire1 {
		steps2, present := wire2[pos]
		if present {
			dist := steps1 + steps2
			if best == -1 || dist < best {
				best = dist
			}
		}
	}

	println("The answer to part two is " + strconv.Itoa(best))
}
