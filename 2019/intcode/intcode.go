package intcode

import (
	"strconv"
	"strings"
)

// Parse decodes an Intcode program
func Parse(input string) []int {
	program := []int{}
	for _, line := range strings.Split(input, ",") {
		val, _ := strconv.Atoi(line)
		program = append(program, val)
	}
	return program
}

func getParams(program []int, instructionIdx int, parameterCount int) []int {
	params := []int{}
	modes := program[instructionIdx] / 100
	for paramIdx := 0; paramIdx < parameterCount; paramIdx++ {
		parameter := program[instructionIdx+paramIdx+1]
		switch modes % 10 {
		case 0:
			parameter = program[parameter]
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

// Execute runs an Intcode program
func Execute(program []int, input chan int) chan int {
	// Copy to avoid messing with the original program
	program = append([]int{}, program...)
	output := make(chan int)
	impl := func() {
		instructionIdx := 0

		read := func(paramCount int) []int {
			return getParams(program, instructionIdx, paramCount)
		}
		write := func(outParameterIdx int, value int) {
			program[program[instructionIdx+outParameterIdx+1]] = value
		}
		for {
			switch program[instructionIdx] % 100 {
			case 1:
				params := read(2)
				write(2, params[0]+params[1])
				instructionIdx += 4
			case 2:
				params := read(2)
				write(2, params[0]*params[1])
				instructionIdx += 4
			case 3:
				write(0, <-input)
				instructionIdx += 2
			case 4:
				params := read(1)
				output <- params[0]
				instructionIdx += 2
			case 5:
				params := read(2)
				if params[0] != 0 {
					instructionIdx = params[1]
				} else {
					instructionIdx += 3
				}
			case 6:
				params := read(2)
				if params[0] == 0 {
					instructionIdx = params[1]
				} else {
					instructionIdx += 3
				}
			case 7:
				params := read(2)
				val := 0
				if params[0] < params[1] {
					val = 1
				}
				write(2, val)
				instructionIdx += 4
			case 8:
				params := read(2)
				val := 0
				if params[0] == params[1] {
					val = 1
				}
				write(2, val)
				instructionIdx += 4
			case 99:
				close(output)
				return
			default:
				panic("Something broke!")
			}
		}
	}
	go impl()
	return output
}
