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

func countCombinations2(bestContainers int, currentContainers int, containers []int, remaining int) (int, int) {
	if currentContainers > bestContainers {
		return 0, bestContainers
	}
	if 0 == len(containers) {
		if 0 == remaining {
			return 1, currentContainers
		}
		return 0, bestContainers
	}
	count := 0
	if remaining >= containers[0] {
		subCount, subBestContainers := countCombinations2(bestContainers, currentContainers+1, containers[1:], remaining-containers[0])
		if subBestContainers < bestContainers {
			bestContainers = subBestContainers
			count = 0
		}
		count += subCount
	}
	subCount, subBestContainers := countCombinations2(bestContainers, currentContainers, containers[1:], remaining)
	if subBestContainers < bestContainers {
		bestContainers = subBestContainers
		count = 0
	}
	count += subCount
	return count, bestContainers
}

func part2(input string) {
	containers := parse(input)
	combinations, _ := countCombinations2(len(containers), 0, containers, 150)
	println("The answer to part two is " + strconv.Itoa(combinations))
}
