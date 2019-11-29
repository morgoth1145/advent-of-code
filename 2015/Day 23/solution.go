package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 23)
	part1(input)
	part2(input)
}

func runInstructions(instructions []string, a int, b int) (int, int) {
	instructionIdx := 0
	for instructionIdx < len(instructions) {
		parts := strings.Split(instructions[instructionIdx], " ")
		switch parts[0] {
		case "hlf":
			switch parts[1] {
			case "a":
				a /= 2
			case "b":
				b /= 2
			}
		case "tpl":
			switch parts[1] {
			case "a":
				a *= 3
			case "b":
				b *= 3
			}
		case "inc":
			switch parts[1] {
			case "a":
				a++
			case "b":
				b++
			}
		case "jmp":
			off, _ := strconv.Atoi(parts[1])
			instructionIdx += off
			continue
		case "jie":
			shouldJump := false
			switch parts[1] {
			case "a,":
				shouldJump = 0 == a%2
			case "b,":
				shouldJump = 0 == b%2
			}
			if shouldJump {
				off, _ := strconv.Atoi(parts[2])
				instructionIdx += off
				continue
			}
		case "jio":
			shouldJump := false
			switch parts[1] {
			case "a,":
				shouldJump = 1 == a
			case "b,":
				shouldJump = 1 == b
			}
			if shouldJump {
				off, _ := strconv.Atoi(parts[2])
				instructionIdx += off
				continue
			}
		}
		instructionIdx++
	}
	return a, b
}

func part1(input string) {
	instructions := strings.Split(input, "\n")
	_, b := runInstructions(instructions, 0, 0)
	println("The answer to part one is " + strconv.Itoa(b))
}

func part2(input string) {
	instructions := strings.Split(input, "\n")
	_, b := runInstructions(instructions, 1, 0)
	println("The answer to part two is " + strconv.Itoa(b))
}
