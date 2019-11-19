package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 1)
	part1(input)
}

func part1(input string) {
	println("The answer to part one is " + strconv.Itoa(strings.Count(input, "(")-strings.Count(input, ")")))
}
