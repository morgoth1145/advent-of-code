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

func decomposeSequence(sequence string, maxLength int) (string, string, string, string) {
	findCandidates := func(subSequence string) []string {
		parts := strings.Split(subSequence, ",")
		candidates := []string{}
		current := parts[0]
		parts = parts[1:]
		for len(current) <= maxLength {
			candidates = append(candidates, current)
			if len(parts) == 0 {
				break
			}
			current += "," + parts[0]
			parts = parts[1:]
		}
		return candidates
	}
	getCandidateBestOrder := func(candidates []string, curSequence string) []string {
		numOccuranceToCandidates := map[int][]string{}
		mostOccurances := 0
		for _, c := range candidates {
			count := strings.Count(curSequence, c)
			numOccuranceToCandidates[count] = append(numOccuranceToCandidates[count], c)
			if count > mostOccurances {
				mostOccurances = count
			}
		}
		out := []string{}
		for count := mostOccurances; count > 0; count-- {
			candidatesForCount := numOccuranceToCandidates[count]
			for idx := len(candidatesForCount) - 1; idx >= 0; idx-- {
				out = append(out, candidatesForCount[idx])
			}
		}
		return out
	}
	getCandidateSlice := func(curSequence string) string {
		parts := strings.Split(curSequence, ",")
		for len(parts) > 0 && (parts[0] == "A" || parts[0] == "B") {
			parts = parts[1:]
		}
		goodParts := []string{}
		for _, p := range parts {
			if p == "A" || p == "B" {
				break
			}
			goodParts = append(goodParts, p)
		}
		return strings.Join(goodParts, ",")
	}
	isMainSequenceValid := func(mainSequence string) bool {
		if len(mainSequence) > maxLength {
			return false
		}
		for _, c := range mainSequence {
			switch c {
			case 'A', 'B', 'C', ',':
				break
			default:
				return false
			}
		}
		return true
	}
	for _, aSequence := range getCandidateBestOrder(findCandidates(sequence), sequence) {
		aReplacedSequence := strings.ReplaceAll(sequence, aSequence, "A")
		for _, bSequence := range getCandidateBestOrder(findCandidates(getCandidateSlice(aReplacedSequence)), aReplacedSequence) {
			bReplacedSequence := strings.ReplaceAll(aReplacedSequence, bSequence, "B")
			for _, cSequence := range getCandidateBestOrder(findCandidates(getCandidateSlice(bReplacedSequence)), bReplacedSequence) {
				cReplacedSequence := strings.ReplaceAll(bReplacedSequence, cSequence, "C")
				if isMainSequenceValid(cReplacedSequence) {
					return cReplacedSequence, aSequence, bSequence, cSequence
				}
			}
		}
	}
	panic("No solution found!")
}

func part2(input string) {
	roboChan := make(chan int64)
	program := intcode.Parse(input)
	program.Memory[0] = 2
	outChan := program.AsyncRun(intcode.InputChannelFunction(roboChan, intcode.EOFPanic))
	tiles := parseTileMap(readTileMap(outChan))

	go func() {
		mainSequence, aSequence, bSequence, cSequence := decomposeSequence(findFullSequence(tiles), 20)
		robotInput := mainSequence + "\n" + aSequence + "\n" + bSequence + "\n" + cSequence + "\n" + "n\n"

		for _, c := range robotInput {
			roboChan <- int64(c)
		}
		close(roboChan)
	}()

	// Apparently the tiles are given to us two more times? I don't care about that, I have the info that I need!
	readTileMap(outChan)
	readTileMap(outChan)

	println("The answer to part two is " + strconv.FormatInt(<-outChan, 10))
}
