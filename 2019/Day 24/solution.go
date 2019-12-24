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

func countSurrounding(pos vector2D, tiles map[vector2D]bool) int {
	out := 0
	for _, n := range surroundingTiles(pos) {
		if tiles[n] {
			out++
		}
	}
	return out
}

func iterate(tiles map[vector2D]bool) map[vector2D]bool {
	out := map[vector2D]bool{}
	for pos, bug := range tiles {
		neighborCount := countSurrounding(pos, tiles)
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

func getBoundingBox(tiles map[vector2D]bool) (vector2D, vector2D) {
	min, max := vector2D{0, 0}, vector2D{0, 0}
	for p := range tiles {
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
	// I wasted a few minutes due to using the wrong ranges here. Maybe 3-4?
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

type vector3D struct {
	x int
	y int
	z int
}

func parse2(input string) map[vector3D]bool {
	out := map[vector3D]bool{}
	for y, line := range strings.Split(input, "\n") {
		for x, c := range line {
			if x == 2 && y == 2 {
				continue
			}
			if c == '#' {
				out[vector3D{x, y, 0}] = true
			} else {
				out[vector3D{x, y, 0}] = false
			}
		}
	}
	return out
}

func surroundingTiles2(pos vector3D) []vector3D {
	out := []vector3D{}
	for _, pos2D := range surroundingTiles(vector2D{pos.x, pos.y}) {
		if pos2D.x == 2 && pos2D.y == 2 {
			// Go *IN* one level
			if pos.x == 2 {
				// x varies
				y := 0
				if pos.y == 3 {
					y = 4
				}
				for x := 0; x < 5; x++ {
					out = append(out, vector3D{x, y, pos.z - 1})
				}
			} else {
				// y varies
				x := 0
				if pos.x == 3 {
					x = 4
				}
				for y := 0; y < 5; y++ {
					out = append(out, vector3D{x, y, pos.z - 1})
				}
			}
			continue
		}
		// Go *OUT* one level special cases
		if pos2D.x < 0 {
			out = append(out, vector3D{1, 2, pos.z + 1})
			continue
		} else if pos2D.x > 4 {
			out = append(out, vector3D{3, 2, pos.z + 1})
			continue
		}
		if pos2D.y < 0 {
			out = append(out, vector3D{2, 1, pos.z + 1})
			continue
		} else if pos2D.y > 4 {
			out = append(out, vector3D{2, 3, pos.z + 1})
			continue
		}
		out = append(out, vector3D{pos2D.x, pos2D.y, pos.z})
	}
	return out
}

func countSurrounding2(pos vector3D, tiles map[vector3D]bool) int {
	out := 0
	for _, n := range surroundingTiles2(pos) {
		if tiles[n] {
			out++
		}
	}
	return out
}

func getTilesToProcess2(tiles map[vector3D]bool) []vector3D {
	shouldHandle := map[vector3D]bool{}
	for pos, bug := range tiles {
		if bug {
			shouldHandle[pos] = true
			for _, n := range surroundingTiles2(pos) {
				shouldHandle[n] = true
			}
		}
	}
	out := []vector3D{}
	for pos := range shouldHandle {
		out = append(out, pos)
	}
	return out
}

func iterate2(tiles map[vector3D]bool) map[vector3D]bool {
	out := map[vector3D]bool{}
	for _, pos := range getTilesToProcess2(tiles) {
		bug := tiles[pos]
		neighborCount := countSurrounding2(pos, tiles)
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

func part2(input string) {
	tiles := parse2(input)
	for i := 0; i < 200; i++ {
		tiles = iterate2(tiles)
	}
	count := 0
	for _, bug := range tiles {
		if bug {
			count++
		}
	}
	println("The answer to part two is " + strconv.Itoa(count))
}
