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

func move(x int, y int, c rune) (int, int) {
	if '<' == c {
		x--
	} else if '>' == c {
		x++
	} else if '^' == c {
		y++
	} else if 'v' == c {
		y--
	}
	return x, y
}

func part1(input string) {
	m := make(map[string]int)
	m["0,0"] = 1
	x, y := 0, 0
	for _, c := range input {
		x, y = move(x, y, c)
		pos := strconv.Itoa(x) + "," + strconv.Itoa(y)
		m[pos]++
	}
	println("The answer to part one is " + strconv.Itoa(len(m)))
}

func part2(input string) {
	m := make(map[string]int)
	m["0,0"] = 2
	x1, y1 := 0, 0
	x2, y2 := 0, 0
	for idx, c := range input {
		if 0 == idx%2 {
			x2, y2 = move(x2, y2, c)
			pos := strconv.Itoa(x2) + "," + strconv.Itoa(y2)
			m[pos]++
		} else {
			x1, y1 = move(x1, y1, c)
			pos := strconv.Itoa(x1) + "," + strconv.Itoa(y1)
			m[pos]++
		}
	}
	println("The answer to part one is " + strconv.Itoa(len(m)))
}
