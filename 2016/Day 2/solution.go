package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2016, 2)
	part1(input)
	part2(input)
}

func doSequence(sequence string, x int, y int, validityCheck func(int, int) bool) (int, int) {
	for _, c := range sequence {
		switch c {
		case 'U':
			y--
			if !validityCheck(x, y) {
				y++
			}
		case 'D':
			y++
			if !validityCheck(x, y) {
				y--
			}
		case 'L':
			x--
			if !validityCheck(x, y) {
				x++
			}
		case 'R':
			x++
			if !validityCheck(x, y) {
				x--
			}
		}
	}
	return x, y
}

func getValue(x int, y int, width int, height int) int {
	return 1 + x + width*y
}

func part1(input string) {
	x, y := 1, 1
	code := 0
	for _, line := range strings.Split(input, "\n") {
		x, y = doSequence(line, x, y, func(x int, y int) bool {
			return x >= 0 && x < 3 && y >= 0 && y < 3
		})
		code = 10*code + 1 + x + y*3
	}
	println("The answer to part one is " + strconv.Itoa(code))
}

func part2(input string) {
}
