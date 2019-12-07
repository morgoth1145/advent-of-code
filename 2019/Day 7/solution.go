package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 7)
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

func execute(codes []int, input chan int) chan int {
	// Copy to avoid messing with the original codes
	codes = append([]int{}, codes...)
	output := make(chan int)
	impl := func() {
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
				write(0, <-input)
				instructionIdx += 2
			case 4:
				params := getParams(1)
				output <- params[0]
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

func listChannel(items ...int) chan int {
	out := make(chan int, len(items))
	for _, v := range items {
		out <- v
	}
	close(out)
	return out
}

func chainChannel(inputs ...chan int) chan int {
	out := make(chan int, 1)
	impl := func() {
		for _, c := range inputs {
			for v := range c {
				out <- v
			}
		}
		close(out)
	}
	go impl()
	return out
}

func permutations(values []int) chan []int {
	out := make(chan []int)
	var impl func(int)
	impl = func(idx int) {
		if idx == len(values) {
			out <- append([]int{}, values...)
			return
		}
		impl(idx + 1)
		for j := idx + 1; j < len(values); j++ {
			values[idx], values[j] = values[j], values[idx]
			impl(idx + 1)
			values[idx], values[j] = values[j], values[idx]
		}
		if 0 == idx {
			close(out)
		}
	}
	go impl(0)
	return out
}

func part1(input string) {
	codes := parse(input)
	best := -1
	for sequence := range permutations([]int{0, 1, 2, 3, 4}) {
		lastAmplifierOutput := listChannel(0)
		for _, phase := range sequence {
			lastAmplifierOutput = execute(codes, chainChannel(listChannel(phase), lastAmplifierOutput))
		}
		output := <-lastAmplifierOutput
		if best == -1 || best < output {
			best = output
		}
	}
	println("The answer to part one is " + strconv.Itoa(best))
}

func part2(input string) {
}
