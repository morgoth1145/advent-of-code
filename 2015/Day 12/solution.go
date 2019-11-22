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

func readJSONInt(input []rune) (int, []rune) {
	negative := false
	if input[0] == '-' {
		negative = true
		input = input[1:]
	}
	value := 0
	for idx, c := range input {
		switch c {
		case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
			value = 10*value + (int(c) - int('0'))
		default:
			if negative {
				return -1 * value, input[idx:]
			}
			return value, input[idx:]
		}
	}
	return 0, []rune{}
}

func readJSONString(input []rune) (string, []rune) {
	input = input[1:] // Skip first quote
	for idx, c := range input {
		if c == '"' {
			return string(input[:idx]), input[idx+1:]
		}
	}
	return string(input), []rune{}
}

func sumJSONIntsList(input []rune) (int, []rune) {
	input = input[1:] // Skip first bracket
	total := 0
	for {
		c := input[0]
		switch c {
		case ',':
			input = input[1:]
			continue
		case ']':
			return total, input[1:]
		default:
			value, rest := sumJSONInts(input)
			total += value
			input = rest
		}
	}
}

func sumJSONIntsObject(input []rune) (int, []rune) {
	input = input[1:] // Skip first brace
	total := 0
	for {
		c := input[0]
		switch c {
		case '}':
			return total, input[1:]
		case ',':
			input = input[1:]
		default:
			_, rest := readJSONString(input)   // Key
			input = rest[1:]                   // Skip :
			value, rest2 := sumJSONInts(input) // Value
			total += value
			input = rest2
		}
	}
}

func sumJSONInts(input []rune) (int, []rune) {
	c := input[0]
	switch c {
	case '[':
		return sumJSONIntsList(input)
	case '"':
		_, rest := readJSONString(input)
		return 0, rest
	case '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
		return readJSONInt(input)
	case '{':
		return sumJSONIntsObject(input)
	default:
		return 0, []rune{}
	}
}

func part1(input string) {
	total, _ := sumJSONInts([]rune(input))
	println("The answer to part one is " + strconv.Itoa(total))
}

func part2(input string) {
}
