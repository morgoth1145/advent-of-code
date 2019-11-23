package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 13)
	part1(input)
	part2(input)
}

type peoplePair [2]string

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

func parse(input string) ([]string, map[peoplePair]int) {
	people := []string{}
	scores := map[peoplePair]int{}
	for _, line := range strings.Split(input, "\n") {
		parts := strings.Split(line, " ")
		p1 := parts[0]
		direction := parts[2]
		amount, _ := strconv.Atoi(parts[3])
		p2 := parts[10]
		p2 = p2[:len(p2)-1] // Remove period

		if direction == "lose" {
			amount *= -1
		}

		scores[peoplePair{p1, p2}] = amount
		people = append(people, p1)
	}
	people = unique(people)
	return people, scores
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
	people, scores := parse(input)
	bestScore := 0
	generatePermutations(people, func(permutation []string) {
		score := 0
		for idx := 0; idx < len(permutation); idx++ {
			nextIdx := (idx + 1) % len(permutation)
			s1 := scores[peoplePair{permutation[idx], permutation[nextIdx]}]
			s2 := scores[peoplePair{permutation[nextIdx], permutation[idx]}]
			score += s1
			score += s2
		}
		if score > bestScore {
			bestScore = score
		}
	})
	println("The answer to part one is " + strconv.Itoa(bestScore))
}

func part2(input string) {
}
