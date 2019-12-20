package main

import (
	"advent-of-code/2019/channeltypes"
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 19)
	part1(input)
	part2(input)
}

func isSquareAffected(x int, y int, program intcode.Program) bool {
	coordInputs := channeltypes.List(int64(x), int64(y))
	affected := program.Clone().AsyncRun(intcode.InputChannelFunction(coordInputs, intcode.EOFPanic))
	if 1 == <-affected {
		return true
	}
	return false
}

func part1(input string) {
	program := intcode.Parse(input)
	totalAffected := 0
	for x := 0; x < 50; x++ {
		for y := 0; y < 50; y++ {
			if isSquareAffected(x, y, program) {
				totalAffected++
			}
		}
	}
	println("The answer to part one is " + strconv.Itoa(totalAffected))
}

func part2(input string) {
	program := intcode.Parse(input)
	x := 0
	y := 0
	for !isSquareAffected(x+99, y, program) {
		y++
		for !isSquareAffected(x, y+99, program) {
			x++
		}
	}
	println("The answer to part two is " + strconv.Itoa(x*10000+y))
}
