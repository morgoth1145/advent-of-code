package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 17)
	part1(input)
	part2(input)
}

type vector2D struct {
	x int
	y int
}

func parseTileMap(input string) map[vector2D]rune {
	tiles := map[vector2D]rune{}
	for y, line := range strings.Split(input, "\n") {
		for x, c := range line {
			tiles[vector2D{x, y}] = c
		}
	}
	return tiles
}

func surroundingTiles(pos vector2D) []vector2D {
	return []vector2D{
		vector2D{pos.x - 1, pos.y},
		vector2D{pos.x + 1, pos.y},
		vector2D{pos.x, pos.y - 1},
		vector2D{pos.x, pos.y + 1},
	}
}

func part1(input string) {
	program := intcode.Parse(input)
	tileMap := ""
	for c := range program.AsyncRun(nil) {
		tileMap += string(c)
	}
	tiles := parseTileMap(tileMap)
	alignTotal := 0
	for pos, tile := range tiles {
		if tile == '#' {
			allSurrounding := true
			for _, n := range surroundingTiles(pos) {
				if tiles[n] != '#' {
					allSurrounding = false
					break
				}
			}
			if allSurrounding {
				alignTotal += pos.x * pos.y
			}
		}
	}
	println("The answer to part one is " + strconv.Itoa(alignTotal))
}

func part2(input string) {
}
