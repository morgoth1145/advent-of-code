package main

import (
	"advent-of-code/aochelpers"
	"advent-of-code/helpers"
	"math"
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

func getVisibleAngles(c vector2D, asteroids map[vector2D]bool) map[vector2D]bool {
	seen := map[vector2D]bool{}
	for other := range asteroids {
		if c == other {
			continue
		}

		angle := vector2D{x: other.x - c.x, y: other.y - c.y}
		denominator := helpers.GCD(helpers.Abs(angle.x), helpers.Abs(angle.y))
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
	asteroids := parse(input)
	chosenAngles := map[vector2D]bool{}
	var chosenCoord vector2D
	for c := range asteroids {
		newAngles := getVisibleAngles(c, asteroids)
		if len(newAngles) > len(chosenAngles) {
			chosenAngles = newAngles
			chosenCoord = c
		}
	}
	angle := vector2D{x: 0, y: -1}
	destroyed := 0
	for {
		for mult := 1; mult < 100; mult++ {
			c := vector2D{x: chosenCoord.x + angle.x*mult, y: chosenCoord.y + angle.y*mult}
			_, present := asteroids[c]
			if present {
				destroyed++
				delete(asteroids, c)
				if 200 == destroyed {
					println("The answer to part one is " + strconv.Itoa(c.x*100+c.y))
					return
				}
				break
			}
		}
		var nextAngle vector2D
		bestDiff := 2 * math.Pi
		curDeg := math.Atan2(float64(angle.y), float64(angle.x))
		if curDeg < 0 {
			curDeg += 2 * math.Pi
		}
		for a := range chosenAngles {
			if angle == a {
				continue
			}
			aDeg := math.Atan2(float64(a.y), float64(a.x))
			for curDeg > aDeg {
				aDeg += 2 * math.Pi
			}
			if aDeg-curDeg < bestDiff {
				bestDiff = aDeg - curDeg
				nextAngle = a
			}
		}
		angle = nextAngle
	}
}
