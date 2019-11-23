package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 16)
	part1(input)
	part2(input)
}

type auntStats struct {
	number      int
	children    int
	cats        int
	samoyeds    int
	pomeranians int
	akitas      int
	vizslas     int
	goldfish    int
	trees       int
	cars        int
	perfumes    int
}

func stripCharacter(s string, c byte) string {
	if s[len(s)-1] == c {
		return s[:len(s)-1]
	}
	return s
}

func parse(input string) []auntStats {
	aunts := []auntStats{}
	for _, line := range strings.Split(input, "\n") {
		stats := auntStats{}
		stats.children = -1
		stats.cats = -1
		stats.samoyeds = -1
		stats.pomeranians = -1
		stats.akitas = -1
		stats.vizslas = -1
		stats.goldfish = -1
		stats.trees = -1
		stats.cars = -1
		stats.perfumes = -1

		parts := strings.Split(line, " ")
		stats.number, _ = strconv.Atoi(stripCharacter(parts[1], ':'))
		parts = parts[2:]
		for len(parts) > 0 {
			key := stripCharacter(parts[0], ':')
			value, _ := strconv.Atoi(stripCharacter(parts[1], ','))
			parts = parts[2:]
			switch key {
			case "children":
				stats.children = value
			case "cats":
				stats.cats = value
			case "samoyeds":
				stats.samoyeds = value
			case "pomeranians":
				stats.pomeranians = value
			case "akitas":
				stats.akitas = value
			case "vizslas":
				stats.vizslas = value
			case "goldfish":
				stats.goldfish = value
			case "trees":
				stats.trees = value
			case "cars":
				stats.cars = value
			case "perfumes":
				stats.perfumes = value
			}
		}
		aunts = append(aunts, stats)
	}
	return aunts
}

func part1(input string) {
	aunts := parse(input)
	for _, aunt := range aunts {
		if aunt.children != -1 && aunt.children != 3 {
			continue
		}
		if aunt.cats != -1 && aunt.cats != 7 {
			continue
		}
		if aunt.samoyeds != -1 && aunt.samoyeds != 2 {
			continue
		}
		if aunt.pomeranians != -1 && aunt.pomeranians != 3 {
			continue
		}
		if aunt.akitas != -1 && aunt.akitas != 0 {
			continue
		}
		if aunt.vizslas != -1 && aunt.vizslas != 0 {
			continue
		}
		if aunt.goldfish != -1 && aunt.goldfish != 5 {
			continue
		}
		if aunt.trees != -1 && aunt.trees != 3 {
			continue
		}
		if aunt.cars != -1 && aunt.cars != 2 {
			continue
		}
		if aunt.perfumes != -1 && aunt.perfumes != 1 {
			continue
		}
		// We have a match!
		println("The answer to part one is " + strconv.Itoa(aunt.number))
	}
}

func part2(input string) {
	aunts := parse(input)
	for _, aunt := range aunts {
		if aunt.children != -1 && aunt.children != 3 {
			continue
		}
		if aunt.cats != -1 && aunt.cats <= 7 {
			continue
		}
		if aunt.samoyeds != -1 && aunt.samoyeds != 2 {
			continue
		}
		if aunt.pomeranians != -1 && aunt.pomeranians >= 3 {
			continue
		}
		if aunt.akitas != -1 && aunt.akitas != 0 {
			continue
		}
		if aunt.vizslas != -1 && aunt.vizslas != 0 {
			continue
		}
		if aunt.goldfish != -1 && aunt.goldfish >= 5 {
			continue
		}
		if aunt.trees != -1 && aunt.trees <= 3 {
			continue
		}
		if aunt.cars != -1 && aunt.cars != 2 {
			continue
		}
		if aunt.perfumes != -1 && aunt.perfumes != 1 {
			continue
		}
		// We have a match!
		println("The answer to part two is " + strconv.Itoa(aunt.number))
	}
}
