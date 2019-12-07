package main

import (
	"advent-of-code/2019/channeltypes"
	"advent-of-code/2019/helpers"
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 7)
	part1(input)
	part2(input)
}

func part1(input string) {
	program := intcode.Parse(input)
	best := -1
	for sequence := range helpers.IntPermutations(0, 1, 2, 3, 4) {
		lastAmplifierOutput := channeltypes.List(0)
		for _, phase := range sequence {
			lastAmplifierOutput = intcode.Execute(program, channeltypes.Chain(channeltypes.List(phase), lastAmplifierOutput))
		}
		output := <-lastAmplifierOutput
		if best == -1 || best < output {
			best = output
		}
	}
	println("The answer to part one is " + strconv.Itoa(best))
}

func part2(input string) {
	codes := intcode.Parse(input)
	best := -1
	for sequence := range helpers.IntPermutations(5, 6, 7, 8, 9) {
		amplifierInput := make(chan int)
		lastAmplifierOutput := channeltypes.Chain(channeltypes.List(0), amplifierInput)
		for _, phase := range sequence {
			lastAmplifierOutput = intcode.Execute(codes, channeltypes.Chain(channeltypes.List(phase), lastAmplifierOutput))
		}
		var output int
		for output = range lastAmplifierOutput {
			amplifierInput <- output
		}
		close(amplifierInput)
		if best == -1 || best < output {
			best = output
		}
	}
	println("The answer to part two is " + strconv.Itoa(best))
}
