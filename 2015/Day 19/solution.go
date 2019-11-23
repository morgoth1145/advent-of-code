package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 19)
	part1(input)
	part2(input)
}

type replacement struct {
	before string
	after  string
}

func parse(input string) ([]replacement, string) {
	replacements := []replacement{}
	molecule := ""
	for _, line := range strings.Split(input, "\n") {
		molecule = line
		parts := strings.Split(line, " => ")
		if 2 == len(parts) {
			replacements = append(replacements, replacement{before: parts[0], after: parts[1]})
		}
	}
	return replacements, molecule
}

func generateMolecules(r replacement, m string) []string {
	out := []string{}
	parts := strings.Split(m, r.before)
	for idx := 0; idx < len(parts)-1; idx++ {
		newMolecule := ""
		newMolecule += strings.Join(parts[:idx+1], r.before)
		newMolecule += r.after
		newMolecule += strings.Join(parts[idx+1:], r.before)
		out = append(out, newMolecule)
	}
	return out
}

func part1(input string) {
	replacements, molecule := parse(input)
	newMolecules := map[string]bool{}
	for _, r := range replacements {
		for _, m := range generateMolecules(r, molecule) {
			newMolecules[m] = true
		}
	}
	println("The answer to part one is " + strconv.Itoa(len(newMolecules)))
}

func part2(input string) {
}
