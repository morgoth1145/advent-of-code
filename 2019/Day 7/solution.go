package main

import (
	"advent-of-code/2019/channeltypes"
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"advent-of-code/helpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 7)
	part1(input)
	part2(input)
}

func part1(input string) {
	program := intcode.Parse(input)
	best := int64(-1)
	for sequence := range helpers.PermuteInts(0, 1, 2, 3, 4) {
		lastAmplifierOutput := channeltypes.List(int64(0))
		for _, phase := range sequence {
			lastAmplifierOutput = program.AsyncRun(intcode.InputChannelFunction(channeltypes.Chain(channeltypes.List(int64(phase)), lastAmplifierOutput)))
		}
		output := <-lastAmplifierOutput
		if best == -1 || best < output {
			best = output
		}
	}
	println("The answer to part one is " + strconv.FormatInt(best, 10))
}

func part2(input string) {
	program := intcode.Parse(input)
	best := int64(-1)
	for sequence := range helpers.PermuteInts(5, 6, 7, 8, 9) {
		amplifierInput := make(chan int64)
		lastAmplifierOutput := channeltypes.Chain(channeltypes.List(int64(0)), amplifierInput)
		for _, phase := range sequence {
			lastAmplifierOutput = program.AsyncRun(intcode.InputChannelFunction(channeltypes.Chain(channeltypes.List(int64(phase)), lastAmplifierOutput)))
		}
		var output int64
		for output = range lastAmplifierOutput {
			amplifierInput <- output
		}
		close(amplifierInput)
		if best == -1 || best < output {
			best = output
		}
	}
	println("The answer to part two is " + strconv.FormatInt(best, 10))
}
