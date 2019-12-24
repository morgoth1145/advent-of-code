package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 24)
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
				out[vector2D{x, y}] = true
			} else {
				out[vector2D{x, y}] = false
			}
		}
	}
	return out
}

func surroundingTiles(pos vector2D) []vector2D {
	return []vector2D{
		vector2D{pos.x - 1, pos.y},
		vector2D{pos.x + 1, pos.y},
		vector2D{pos.x, pos.y - 1},
		vector2D{pos.x, pos.y + 1},
	}
}

func iterate(bugs map[vector2D]bool) map[vector2D]bool {
	out := map[vector2D]bool{}
	for pos, bug := range bugs {
		neighborCount := 0
		for _, n := range surroundingTiles(pos) {
			if bugs[n] {
				neighborCount++
			}
		}
		if bug {
			if 1 == neighborCount {
				out[pos] = true
			} else {
				out[pos] = false
			}
		} else {
			if 1 == neighborCount || 2 == neighborCount {
				out[pos] = true
			} else {
				out[pos] = false
			}
		}
	}
	return out
}

func getBoundingBox(bugs map[vector2D]bool) (vector2D, vector2D) {
	min, max := vector2D{0, 0}, vector2D{0, 0}
	for p := range bugs {
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

func calcBiodiversity(tiles map[vector2D]bool) int {
	out := 0
	mask := 1
	min, max := getBoundingBox(tiles)
	for y := min.y; y <= max.y; y++ {
		for x := min.x; x <= max.x; x++ {
			if tiles[vector2D{x, y}] {
				out += mask
			}
			mask *= 2
		}
	}
	return out
}

func part1(input string) {
	tiles := parse(input)
	seen := map[int]bool{}
	seen[calcBiodiversity(tiles)] = true
	for {
		tiles = iterate(tiles)
		biodiversity := calcBiodiversity(tiles)
		if seen[biodiversity] {
			println("The answer to part one is " + strconv.Itoa(biodiversity))
			return
		}
		seen[biodiversity] = true
	}
}

func part2(input string) {
}
