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

func getDiagnostic(output <-chan int64) int64 {
	last := int64(0)
	for v := range output {
		if last != 0 {
			panic("Invalid output!")
		}
		last = v
	}
	return last
}

func part1(input string) {
	output := getDiagnostic(intcode.Parse(input).AsyncRun(intcode.InputChannelFunction(channeltypes.List(int64(1)))))
	println("The answer to part one is " + strconv.FormatInt(output, 10))
}

func part2(input string) {
	output := getDiagnostic(intcode.Parse(input).AsyncRun(intcode.InputChannelFunction(channeltypes.List(int64(5)))))
	println("The answer to part two is " + strconv.FormatInt(output, 10))
}
