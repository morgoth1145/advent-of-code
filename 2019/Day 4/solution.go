package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 4)
	part1(input)
	part2(input)
}

func parse(input string) (int, int) {
	parts := strings.Split(input, "-")
	v1, _ := strconv.Atoi(parts[0])
	v2, _ := strconv.Atoi(parts[1])
	return v1, v2
}

func getDigits(n int) []int {
	out := []int{}
	for n > 0 {
		d := n % 10
		n /= 10
		out = append(append([]int{}, d), out...)
	}
	return out
}

func validate(n int) bool {
	c := -1
	hasDouble := false
	for _, d := range getDigits(n) {
		if d == c {
			hasDouble = true
		} else if d < c {
			return false // Decreasing
		}
		c = d
	}
	return hasDouble
}

func part1(input string) {
	low, high := parse(input)
	valid := 0
	for i := low; i <= high; i++ {
		if validate(i) {
			valid++
		}
	}
	println("The answer to part one is " + strconv.Itoa(valid))
}

func validate2(n int) bool {
	c := -1
	doubleDigit := -1
	doubleDigitCount := 0
	for _, d := range getDigits(n) {
		if d < c {
			return false // Decreasing
		} else if d == c {
			if doubleDigit == d {
				doubleDigitCount++
			} else if doubleDigit == -1 || doubleDigitCount != 1 {
				doubleDigit = d
				doubleDigitCount = 1
			}
		}
		c = d
	}
	return doubleDigit != -1 && doubleDigitCount == 1
}

func part2(input string) {
	low, high := parse(input)
	valid := 0
	for i := low; i <= high; i++ {
		if validate2(i) {
			valid++
		}
	}
	println("The answer to part two is " + strconv.Itoa(valid))
}
