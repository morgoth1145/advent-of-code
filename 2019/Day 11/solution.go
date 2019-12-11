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

func getBoundingBox(points map[point2D]int64) (point2D, point2D) {
	min, max := point2D{0, 0}, point2D{0, 0}
	for p := range points {
		if p.x < min.x {
			min.x = p.x
		} else if p.x > max.x {
			max.x = p.x
		}
		if p.y < min.y {
			min.y = p.y
		} else if p.y > max.y {
			max.y = p.y
		}
	}
	return min, max
}

func part2(input string) {
	points := paintHull(input, 1)
	min, max := getBoundingBox(points)
	println("The answer to part two is an image:")
	for y := max.y; y >= min.y; y-- {
		line := ""
		for x := min.x; x <= max.x; x++ {
			if points[point2D{x, y}] == 0 {
				line += " "
			} else {
				line += "\u2588"
			}
		}
		println(line)
	}
}
