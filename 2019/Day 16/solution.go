package main

import (
	"advent-of-code/aochelpers"
	"advent-of-code/helpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 16)
	part1(input)
	part2(input)
}

func parse(input string) []int {
	out := []int{}
	for _, c := range input {
		val, _ := strconv.Atoi(string(c))
		out = append(out, val)
	}
	return out
}

func runPhase(values []int) []int {
	out := []int{}
	for index := 0; index < len(values); index++ {
		val := 0
		for valIdx, v := range values {
			multIdx := valIdx + 1
			multIdx /= (index + 1)
			multIdx %= 4
			switch multIdx {
			case 1:
				val += v
			case 3:
				val -= v
			}
		}
		val = helpers.Abs(val) % 10
		out = append(out, val)
	}
	return out
}

func valuesToString(values []int) string {
	out := ""
	for _, v := range values {
		out += strconv.Itoa(v)
	}
	return out
}

func part1(input string) {
	values := parse(input)
	for i := 0; i < 100; i++ {
		values = runPhase(values)
	}
	println("The answer to part one is " + valuesToString(values[:8]))
}

func part2(input string) {
}
