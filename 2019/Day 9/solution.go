package main

import (
	"advent-of-code/2019/channeltypes"
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 9)
	part1(input)
	part2(input)
}

func part1(input string) {
	output := <-intcode.Parse(input).AsyncRun(channeltypes.List(int64(1)))
	println("The answer to part one is " + strconv.FormatInt(output, 10))
}

func part2(input string) {
}
