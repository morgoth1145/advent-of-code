package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 5)
	part1(input)
	part2(input)
}

func parse(input string) []int {
	out := []int{}
	for _, line := range strings.Split(input, ",") {
		val, _ := strconv.Atoi(line)
		out = append(out, val)
	}
	return out
}

func execute(codes []int, input func() int, output func(int)) []int {
	// Copy to avoid messing with the original codes
	codes = append([]int{}, codes...)
	instructionIdx := 0

	getParams := func(parameterCount int) []int {
		params := []int{}
		modes := codes[instructionIdx] / 100
		for paramIdx := 0; paramIdx < parameterCount; paramIdx++ {
			parameter := codes[instructionIdx+paramIdx+1]
			switch modes % 10 {
			case 0:
				parameter = codes[parameter]
			case 1:
				break // parameter is already correct
			default:
				panic("Unknown mode")
			}
			params = append(params, parameter)
			modes /= 10
		}
		return params
	}
	write := func(outputParameterIdx int, value int) {
		codes[codes[instructionIdx+outputParameterIdx+1]] = value
	}
	for {
		switch codes[instructionIdx] % 100 {
		case 1:
			params := getParams(2)
			write(2, params[0]+params[1])
			instructionIdx += 4
		case 2:
			params := getParams(2)
			write(2, params[0]*params[1])
			instructionIdx += 4
		case 3:
			write(0, input())
			instructionIdx += 2
		case 4:
			params := getParams(1)
			output(params[0])
			instructionIdx += 2
		case 5:
			params := getParams(2)
			if params[0] != 0 {
				instructionIdx = params[1]
			} else {
				instructionIdx += 3
			}
		case 6:
			params := getParams(2)
			if params[0] == 0 {
				instructionIdx = params[1]
			} else {
				instructionIdx += 3
			}
		case 7:
			params := getParams(2)
			val := 0
			if params[0] < params[1] {
				val = 1
			}
			write(2, val)
			instructionIdx += 4
		case 8:
			params := getParams(2)
			val := 0
			if params[0] == params[1] {
				val = 1
			}
			write(2, val)
			instructionIdx += 4
		case 99:
			return codes
		default:
			panic("Something broke!")
		}
	}
}

func getInputMaker(input int) func() int {
	return func() int {
		return input
	}
}

func getOutputAccumulator(output *[]int) func(int) {
	return func(val int) {
		*output = append(*output, val)
	}
}

func getDiagnostic(output []int) int {
	for len(output) > 1 {
		if output[0] != 0 {
			panic("Invalid output!")
		}
		output = output[1:]
	}
	return output[0]
}

func part1(input string) {
	codes := parse(input)
	output := []int{}
	execute(codes, getInputMaker(1), getOutputAccumulator(&output))
	println("The answer to part one is " + strconv.Itoa(getDiagnostic(output)))
}

func part2(input string) {
	codes := parse(input)
	output := []int{}
	execute(codes, getInputMaker(5), getOutputAccumulator(&output))
	println("The answer to part two is " + strconv.Itoa(getDiagnostic(output)))
}
