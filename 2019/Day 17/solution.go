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

func readTileMap(tileChan <-chan int64) string {
	tileMap := ""
	lastC := '\n'
	for c := range tileChan {
		if c == '\n' && lastC == '\n' {
			break // End of map
		}
		tileMap += string(c)
		lastC = rune(c)
	}
	return tileMap
}

func part1(input string) {
	tiles := parseTileMap(readTileMap(intcode.Parse(input).AsyncRun(nil)))
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

func findFullSequence(tiles map[vector2D]rune) string {
	var pos vector2D
	var dir vector2D
	for loc, tile := range tiles {
		switch tile {
		case '^':
			pos = loc
			dir = vector2D{0, -1}
		case 'v':
			pos = loc
			dir = vector2D{0, 1}
		case '<':
			pos = loc
			dir = vector2D{-1, 0}
		case '>':
			pos = loc
			dir = vector2D{1, 0}
		}
	}

	sequence := []string{}
	amount := 0
	for {
		next := vector2D{pos.x + dir.x, pos.y + dir.y}
		if tiles[next] == '#' {
			amount++
			pos = next
			continue
		}
		if amount > 0 {
			sequence = append(sequence, strconv.Itoa(amount))
			amount = 0
		}
		// Try right turn
		dir.x, dir.y = -dir.y, dir.x
		next = vector2D{pos.x + dir.x, pos.y + dir.y}
		if tiles[next] == '#' {
			sequence = append(sequence, "R")
			amount = 1
			pos = next
			continue
		}
		// Try left turn
		dir.x, dir.y = -dir.x, -dir.y
		next = vector2D{pos.x + dir.x, pos.y + dir.y}
		if tiles[next] == '#' {
			sequence = append(sequence, "L")
			amount = 1
			pos = next
			continue
		}
		// We must be at the end!
		break
	}

	return strings.Join(sequence, ",")
}

func part2(input string) {
	roboChan := make(chan int64)
	program := intcode.Parse(input)
	program.Memory[0] = 2
	outChan := program.AsyncRun(intcode.InputChannelFunction(roboChan, intcode.EOFPanic))
	tiles := parseTileMap(readTileMap(outChan))

	go func() {
		println("Sequence: " + findFullSequence(tiles))

		// Solved by hand
		mainSequence := "A,C,C,A,B,A,B,A,B,C"
		aSequence := "R,6,R,6,R,8,L,10,L,4"
		bSequence := "L,4,L,12,R,6,L,10"
		cSequence := "R,6,L,10,R,8"

		for _, c := range mainSequence + "\n" + aSequence + "\n" + bSequence + "\n" + cSequence + "\n" + "n\n" {
			roboChan <- int64(c)
		}
		close(roboChan)
	}()

	// Apparently the tiles are given to us two more times? I don't care about that!
	readTileMap(outChan)
	readTileMap(outChan)

	println("The answer to part two is " + strconv.FormatInt(<-outChan, 10))
}
