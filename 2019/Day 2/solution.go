package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 2)
	part1(input)
	part2(input)
}

func parse(input string) []int {
	program := []int{}
	for _, line := range strings.Split(input, ",") {
		val, _ := strconv.Atoi(line)
		program = append(program, val)
	}
	return program
}

func execute(codes []int) []int {
	// Copy to avoid messing with the original codes
	codes = append([]int{}, codes...)
	instructionIdx := 0

	getParams := func(parameterCount int) []int {
		params := []int{}
		for paramIdx := 0; paramIdx < parameterCount; paramIdx++ {
			parameter := codes[codes[instructionIdx+paramIdx+1]]
			params = append(params, parameter)
		}
		return params
	}
	write := func(outputParameterIdx int, value int) {
		codes[codes[instructionIdx+outputParameterIdx+1]] = value
	}
	for {
		switch codes[instructionIdx] {
		case 1:
			params := getParams(2)
			write(2, params[0]+params[1])
			instructionIdx += 4
		case 2:
			params := getParams(2)
			write(2, params[0]*params[1])
			instructionIdx += 4
		case 99:
			return codes
		default:
			panic("Something broke!")
		}
	}
}

func part1(input string) {
	program := parse(input)
	program[1] = 12
	program[2] = 2
	answer := execute(program)[0]
	println("The answer to part one is " + strconv.Itoa(answer))
}

func part2(input string) {
}
