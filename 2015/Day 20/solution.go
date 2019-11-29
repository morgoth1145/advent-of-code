package main

import (
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2015, 20)
	part1(input)
	part2(input)
}

func part1(input string) {
	value, _ := strconv.Atoi(input)

	powerOfTwoExceedingValue := 1
	for ; (2*powerOfTwoExceedingValue-1)*10 < value; powerOfTwoExceedingValue *= 2 {

	}

	scratch := []int{}
	for i := 0; i < powerOfTwoExceedingValue; i++ {
		scratch = append(scratch, 1)
	}

	best := powerOfTwoExceedingValue

	for i := 1; i < best; i++ {
		for idx := i; idx < best; idx += i {
			scratch[idx] += i * 10
			if scratch[idx] >= value {
				best = idx
			}
		}
	}
	println("The answer to part one is " + strconv.Itoa(best))
}

func part2(input string) {
}
