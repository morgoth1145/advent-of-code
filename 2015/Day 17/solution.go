package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 17)
	part1(input)
	part2(input)
}

func parse(input string) []int {
	containers := []int{}
	for _, line := range strings.Split(input, "\n") {
		size, _ := strconv.Atoi(line)
		containers = append(containers, size)
	}
	return containers
}

func countCombinations(containers []int, remaining int) int {
	if 0 == len(containers) {
		if 0 == remaining {
			return 1
		}
		return 0
	}
	count := 0
	if remaining >= containers[0] {
		count += countCombinations(containers[1:], remaining-containers[0])
	}
	count += countCombinations(containers[1:], remaining)
	return count
}

func part1(input string) {
	containers := parse(input)
	combinations := countCombinations(containers, 150)
	println("The answer to part one is " + strconv.Itoa(combinations))
}

func part2(input string) {
}
