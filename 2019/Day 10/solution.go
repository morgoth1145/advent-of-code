package main

import (
	"advent-of-code/2019/helpers"
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 10)
	part1(input)
	part2(input)
}

type vector2D struct {
	x int
	y int
}

func parse(input string) map[vector2D]bool {
	out := map[vector2D]bool{}
	for y, line := range strings.Split(input, "\n") {
		for x, c := range line {
			if c == '#' {
				out[vector2D{x: x, y: y}] = true
			}
		}
	}
	return out
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func getVisibleAngles(c vector2D, asteroids map[vector2D]bool) map[vector2D]bool {
	seen := map[vector2D]bool{}
	for other := range asteroids {
		if c == other {
			continue
		}

		angle := vector2D{x: other.x - c.x, y: other.y - c.y}
		denominator := gcd(helpers.Abs(angle.x), helpers.Abs(angle.y))
		angle.x /= denominator
		angle.y /= denominator
		seen[angle] = true
	}
	return seen
}

func part1(input string) {
	asteroids := parse(input)
	best := 0
	for c := range asteroids {
		seen := len(getVisibleAngles(c, asteroids))
		if seen > best {
			best = seen
		}
	}
	println("The answer to part one is " + strconv.Itoa(best))
}

func part2(input string) {
}
