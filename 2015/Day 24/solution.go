package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 24)
	part1(input)
	part2(input)
}

func parse(input string) []int {
	out := []int{}
	for _, s := range strings.Split(input, "\n") {
		val, _ := strconv.Atoi(s)
		out = append(out, val)
	}
	return out
}

func reverse(nums []int) []int {
	for i := 0; i < len(nums)/2; i++ {
		j := len(nums) - i - 1
		nums[i], nums[j] = nums[j], nums[i]
	}
	return nums
}

// Prefers smaller early groups
func generateEvenFirstGroupSplit(weights []int, groupCount int, handler func([]int)) {
	totalWeight := 0
	for _, w := range weights {
		totalWeight += w
	}
	var recursivelyGenerateGroup func([]int, []int, int)
	recursivelyGenerateGroup = func(chosen []int, rest []int, remainingWeight int) {
		// if bestLength != -1 && len(chosen) > bestLength {
		// 	return bestLength
		// }
		if 0 == len(rest) {
			if 0 == remainingWeight {
				handler(chosen)
			}
			return
		}
		item := rest[0]
		rest = rest[1:]
		if item <= remainingWeight {
			newChosen := append(append([]int{}, chosen...), item)
			recursivelyGenerateGroup(newChosen, rest, remainingWeight-item)
		}
		recursivelyGenerateGroup(chosen, rest, remainingWeight)
	}
	recursivelyGenerateGroup([]int{}, weights, totalWeight/groupCount)
}

func part1(input string) {
	packages := parse(input)
	bestPackageCount := -1
	bestQuantumEntanglement := -1
	generateEvenFirstGroupSplit(packages, 3, func(group []int) {
		qe := 1
		for _, w := range group {
			qe *= w
		}
		if bestPackageCount == -1 || len(group) < bestPackageCount {
			bestPackageCount = len(group)
			bestQuantumEntanglement = qe
		} else if bestPackageCount == len(group) && qe < bestQuantumEntanglement {
			bestQuantumEntanglement = qe
		}
	})
	println("The answer to part one is " + strconv.Itoa(bestQuantumEntanglement))
}

func part2(input string) {
}
