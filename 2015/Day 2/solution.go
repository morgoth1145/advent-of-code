package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 2)
	part1(input)
	part2(input)
}

func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

func part1(input string) {
	total := 0
	for _, b := range strings.Split(input, "\n") {
		dims := strings.Split(b, "x")
		x, _ := strconv.Atoi(dims[0])
		y, _ := strconv.Atoi(dims[1])
		z, _ := strconv.Atoi(dims[2])
		a := x * y
		b := y * z
		c := z * x
		total += 2*a + 2*b + 2*c + min(a, min(b, c))
	}
	println("The answer to part one is " + strconv.Itoa(total))
}

func part2(input string) {
	total := 0
	for _, b := range strings.Split(input, "\n") {
		dims := strings.Split(b, "x")
		x, _ := strconv.Atoi(dims[0])
		y, _ := strconv.Atoi(dims[1])
		z, _ := strconv.Atoi(dims[2])
		a := 2*x + 2*y
		b := 2*y + 2*z
		c := 2*z + 2*x
		total += min(a, min(b, c)) + x*y*z
	}
	println("The answer to part two is " + strconv.Itoa(total))
}
