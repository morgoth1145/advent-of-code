package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 1)
	part1(input)
	part2(input)
}

func part1(input string) {
	println("The answer to part one is " + strconv.Itoa(strings.Count(input, "(")-strings.Count(input, ")")))
}

func part2(input string) {
	floor := 0
	for idx, c := range input {
		if '(' == c {
			floor++
		} else if ')' == c {
			floor--
			if floor < 0 {
				println("The answer to part two is " + strconv.Itoa(idx+1))
				return
			}
		}
	}
	println("Error, no answer found!")
}
