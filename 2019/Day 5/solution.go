package main

import (
	"advent-of-code/2019/channeltypes"
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 5)
	part1(input)
	part2(input)
}

func getDiagnostic(output <-chan int) int {
	last := 0
	for v := range output {
		if last != 0 {
			panic("Invalid output!")
		}
		last = v
	}
	return last
}

func part1(input string) {
	output := getDiagnostic(intcode.Parse(input).AsyncRun(channeltypes.List(1)))
	println("The answer to part one is " + strconv.Itoa(output))
}

func part2(input string) {
	output := getDiagnostic(intcode.Parse(input).AsyncRun(channeltypes.List(5)))
	println("The answer to part two is " + strconv.Itoa(output))
}
