package main

import (
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2015, 3)
	part1(input)
	part2(input)
}

func part1(input string) {
	m := make(map[string]int)
	m["0,0"] = 1
	x := 0
	y := 0
	for _, c := range input {
		if '<' == c {
			x--
		} else if '>' == c {
			x++
		} else if '^' == c {
			y++
		} else if 'v' == c {
			y--
		}
		pos := strconv.Itoa(x) + "," + strconv.Itoa(y)
		m[pos]++
	}
	println("The answer to part one is " + strconv.Itoa(len(m)))
}

func part2(input string) {
}
