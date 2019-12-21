package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 21)
	part1(input)
	part2(input)
}

func execute(input string, sequence string) int64 {
	springChan := make(chan int64)
	go func() {
		for _, c := range []rune(sequence) {
			springChan <- int64(c)
		}
		close(springChan)
	}()
	var result int64
	for result = range intcode.Parse(input).AsyncRun(intcode.InputChannelFunction(springChan, intcode.EOFPanic)) {
	}
	return result
}

func part1(input string) {
	// Jump if 1-3 tiles away is a gap and 4 tiles away is safe
	instructions := `NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
`
	println("The answer to part one is " + strconv.FormatInt(execute(input, instructions), 10))
}

func part2(input string) {
	// Jump if 1-3 tiles away is a gap, 4 tiles away is safe, and 8 tiles away is safe
	//   OR if 1 tile away is a gap
	instructions := `NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
AND H J
NOT A T
OR T J
RUN
`
	println("The answer to part two is " + strconv.FormatInt(execute(input, instructions), 10))
}
