package main

import (
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2015, 10)
	part1(input)
	part2(input)
}

func parseIntSequence(input string) []uint8 {
	out := []uint8{}
	for _, c := range []rune(input) {
		value, _ := strconv.ParseUint(string(c), 10, 8)
		out = append(out, uint8(value))
	}
	return out
}

func lookAndSay(sequence []uint8) []uint8 {
	out := []uint8{}
	count := uint8(0)
	last := uint8(10)
	for _, i := range sequence {
		if i != last {
			if count > 0 {
				out = append(out, count, last)
			}
			last = i
			count = 0
		}
		count++
	}
	if count > 0 {
		out = append(out, count, last)
	}
	return out
}

func part1(input string) {
	sequence := parseIntSequence(input)
	for iter := 0; iter < 40; iter++ {
		sequence = lookAndSay(sequence)
	}
	println("The answer to part one is " + strconv.Itoa(len(sequence)))
}

func part2(input string) {
}
