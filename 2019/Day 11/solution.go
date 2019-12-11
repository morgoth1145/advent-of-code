package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 11)
	part1(input)
	part2(input)
}

type point2D struct {
	x int
	y int
}

func paintHull(input string, startColor int64) map[point2D]int64 {
	points := map[point2D]int64{}
	p := point2D{0, 0}
	points[p] = startColor
	inputs := make(chan int64, 1)
	inputs <- startColor
	commands := intcode.Parse(input).AsyncRun(inputs)
	vx, vy := 0, 1
	for color := range commands {
		points[p] = color
		if 0 == <-commands {
			vx, vy = -vy, vx
		} else {
			vx, vy = vy, -vx
		}
		p.x += vx
		p.y += vy
		inputs <- points[p]
	}
	return points
}

func part1(input string) {
	println("The answer to part one is " + strconv.Itoa(len(paintHull(input, 0))))
}

func part2(input string) {
}
