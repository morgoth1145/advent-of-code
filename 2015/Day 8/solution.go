package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
	"unicode/utf8"
)

func main() {
	input := aochelpers.GetInput(2015, 8)
	part1(input)
	part2(input)
}

func parseString(s string) string {
	input := []rune(s)
	chars := []rune{}
	for idx := 1; idx < len(input)-1; {
		switch input[idx] {
		case '\\':
			switch input[idx+1] {
			case '\\', '"':
				chars = append(chars, input[idx+1])
				idx += 2
			case 'x':
				val, _ := strconv.ParseInt(string(input[idx+2:idx+4]), 16, 64)
				chars = append(chars, rune(val))
				idx += 4
			}
		default:
			chars = append(chars, input[idx])
			idx++
		}
	}
	return string(chars)
}

func encodeString(s string) string {
	chars := []rune{'"'}
	for _, char := range []rune(s) {
		switch char {
		case '\\', '"':
			chars = append(chars, '\\')
			fallthrough
		default:
			chars = append(chars, char)
		}
	}
	chars = append(chars, '"')
	return string(chars)
}

func part1(input string) {
	difference := 0
	for _, s := range strings.Split(input, "\n") {
		difference += utf8.RuneCountInString(s) - utf8.RuneCountInString(parseString(s))
	}
	println("The answer to part one is " + strconv.Itoa(difference))
}

func part2(input string) {
	difference := 0
	for _, s := range strings.Split(input, "\n") {
		difference += utf8.RuneCountInString(encodeString(s)) - utf8.RuneCountInString(s)
	}
	println("The answer to part one is " + strconv.Itoa(difference))
}
