package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 2)
	part1(input)
	part2(input)
}

func part1(input string) {
	program := intcode.Parse(input)
	program.Memory[1] = 12
	program.Memory[2] = 2
	for range program.AsyncRun(nil) {
	}
	println("The answer to part one is " + strconv.Itoa(int(program.Memory[0])))
}

func part2(input string) {
	program := intcode.Parse(input)
	for noun := 0; noun < 100; noun++ {
		program.Memory[1] = int64(noun)
		for verb := 0; verb < 100; verb++ {
			program.Memory[2] = int64(verb)
			workingProgram := program.Clone()
			for range workingProgram.AsyncRun(nil) {
			}
			if workingProgram.Memory[0] == 19690720 {
				println("The answer to part one is " + strconv.Itoa(100*noun+verb))
				return
			}
		}
	}
	println("Didn't find an answer to part 2!")
}
