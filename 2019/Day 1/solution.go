package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 1)
	part1(input)
	part2(input)
}

func part1(input string) {
	totalFuel := 0
	for _, line := range strings.Split(input, "\n") {
		mass, _ := strconv.Atoi(line)
		fuel := mass/3 - 2
		totalFuel += fuel
	}
	println("The answer to part one is " + strconv.Itoa(totalFuel))
}

func part2(input string) {
	totalFuel := 0
	for _, line := range strings.Split(input, "\n") {
		mass, _ := strconv.Atoi(line)
		for {
			fuel := mass/3 - 2
			if fuel <= 0 {
				break
			}
			totalFuel += fuel
			mass = fuel
		}
	}
	println("The answer to part two is " + strconv.Itoa(totalFuel))
}
