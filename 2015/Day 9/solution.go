package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 9)
	part1(input)
	part2(input)
}

type locationPair [2]string

func unique(items []string) []string {
	seen := map[string]bool{}
	output := []string{}
	for _, i := range items {
		_, present := seen[i]
		if present {
			continue
		}
		seen[i] = true
		output = append(output, i)
	}
	return output
}

func parse(input string) ([]string, map[locationPair]int) {
	locations := []string{}
	distances := map[locationPair]int{}
	for _, line := range strings.Split(input, "\n") {
		parts := strings.Split(line, " = ")
		distance, _ := strconv.Atoi(parts[1])
		parts = strings.Split(parts[0], " to ")
		loc1 := parts[0]
		loc2 := parts[1]
		distances[locationPair{loc1, loc2}] = distance
		distances[locationPair{loc2, loc1}] = distance
		locations = append(locations, loc1)
		locations = append(locations, loc2)
	}
	locations = unique(locations)
	return locations, distances
}

func generatePermutations(items []string, handlePermutation func([]string)) {
	var generate func([]string, []string)
	generate = func(remaining []string, sequence []string) {
		if 0 == len(remaining) {
			handlePermutation(sequence)
			return
		}
		for idx, i := range remaining {
			var newRemaining []string
			if idx < len(remaining) {
				newRemaining = append(append([]string{}, remaining[:idx]...), remaining[idx+1:]...)
			} else {
				newRemaining = remaining[:idx]
			}
			newSequence := append(sequence, i)
			generate(newRemaining, newSequence)
		}
	}
	generate(items, []string{})
}

func part1(input string) {
	locations, distances := parse(input)
	bestDistance := 0
	for _, d := range distances {
		bestDistance += d
	}
	generatePermutations(locations, func(permutation []string) {
		distance := 0
		for idx := 0; idx < len(permutation)-1; idx++ {
			d := distances[locationPair{permutation[idx], permutation[idx+1]}]
			distance += d
		}
		if distance < bestDistance {
			bestDistance = distance
		}
	})
	println("The answer to part one is " + strconv.Itoa(bestDistance))
}

func part2(input string) {
}
