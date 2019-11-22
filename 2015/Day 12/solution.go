package main

import (
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2015, 12)
	part1(input)
	part2(input)
}

func part1(input string) {
	total := 0
	last := -1
	negative := false
	for _, c := range input {
		switch c {
		case '-':
			negative = true
		case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
			val := int(c) - int('0')
			if last == -1 {
				last = val
			} else {
				last = 10*last + val
			}
		default:
			if last != -1 {
				if negative {
					total -= last
				} else {
					total += last
				}
				last = -1
				negative = false
			}
		}
	}
	println("The answer to part one is " + strconv.Itoa(total))
}

func part2(input string) {
}
