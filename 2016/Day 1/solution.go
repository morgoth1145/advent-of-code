package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2016, 1)
	part1(input)
	part2(input)
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func part1(input string) {
	north, east := 0, 0
	northVelocity, eastVelocity := 1, 0
	for _, d := range strings.Split(input, ", ") {
		turn := d[0]
		distance, _ := strconv.Atoi(d[1:])
		if turn == 'L' {
			northVelocity, eastVelocity = eastVelocity, -northVelocity
		} else {
			northVelocity, eastVelocity = -eastVelocity, northVelocity
		}
		north += distance * northVelocity
		east += distance * eastVelocity
	}
	println("The answer to part one is " + strconv.Itoa(abs(north)+abs(east)))
}

func part2(input string) {
}
