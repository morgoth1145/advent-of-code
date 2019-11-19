package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 5)
	part1(input)
	part2(input)
}

func test1(s string) bool {
	vowels := "aeiou"
	count := 0
	for _, c := range s {
		if strings.Contains(vowels, string(c)) {
			count++
			if 3 == count {
				return true
			}
		}
	}
	return false
}

func test2(s string) bool {
	last := rune(s[1])
	for _, c := range s {
		if c == last {
			return true
		}
		last = c
	}
	return false
}

func test3(s string) bool {
	return !strings.Contains(s, "ab") && !strings.Contains(s, "cd") && !strings.Contains(s, "pq") && !strings.Contains(s, "xy")
}

func part1(input string) {
	niceStrings := 0
	for _, s := range strings.Split(input, "\n") {
		if test1(s) && test2(s) && test3(s) {
			niceStrings++
		}
	}
	println("The answer to part one is " + strconv.Itoa(niceStrings))
}

func part2(input string) {
}
