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

	generation := []string{orbits["YOU"]}
	for len(generation) > 0 {
		nextGeneration := []string{}
		for _, obj := range generation {
			transfers := transferCount[obj]
			for objA, orbited := range orbits {
				if objA == obj {
					{
						_, present := transferCount[orbited]
						if present {
							continue
						}
					}
					transferCount[orbited] = transfers + 1
					nextGeneration = append(nextGeneration, orbited)
				}
				if orbited == obj {
					{
						_, present := transferCount[objA]
						if present {
							continue
						}
					}
					transferCount[objA] = transfers + 1
					nextGeneration = append(nextGeneration, objA)
				}
			}
		}
		generation = nextGeneration
	}

	bestTransfers := transferCount[orbits["SAN"]]
	println("The answer to part two is " + strconv.Itoa(bestTransfers))
}
