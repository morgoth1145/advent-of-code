package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 6)
	part1(input)
	part2(input)
}

func parse(input string) map[string]string {
	out := map[string]string{}
	for _, line := range strings.Split(input, "\n") {
		parts := strings.Split(line, ")")
		out[parts[1]] = parts[0]
	}
	return out
}

func part1(input string) {
	orbits := parse(input)

	orbited := map[string][]string{}
	for obj, orbitedObj := range orbits {
		orbited[orbitedObj] = append(orbited[orbitedObj], obj)
	}

	total := 0
	orbitCount := 0
	generation := []string{"COM"}
	for len(generation) > 0 {
		nextGeneration := []string{}
		for _, obj := range generation {
			total += orbitCount
			nextGeneration = append(nextGeneration, orbited[obj]...)
		}
		generation = nextGeneration
		orbitCount++
	}

	println("The answer to part one is " + strconv.Itoa(total))
}

func part2(input string) {
	orbits := parse(input)

	transferCount := map[string]int{}

	start := orbits["YOU"]
	transfers := 0
	for {
		transferCount[start] = transfers
		transfers++
		parent, present := orbits[start]
		if !present {
			break
		}
		start = parent
	}

	target := orbits["SAN"]
	transfers = 0
	for {
		{
			otherTransfers, present := transferCount[target]
			if present {
				transfers += otherTransfers
				break
			}
		}
		transfers++
		parent, present := orbits[target]
		if !present {
			panic("There's no route!")
		}
		target = parent
	}

	println("The answer to part two is " + strconv.Itoa(transfers))
}
