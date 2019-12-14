package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
	"sync"
)

func main() {
	input := aochelpers.GetInput(2019, 13)
	part1(input)
	part2(input)
}

func part1(input string) {
	program := intcode.Parse(input)
	blocks := 0
	outChan := program.AsyncRun(nil)
	for range outChan {
		<-outChan
		tile := <-outChan
		if 2 == tile {
			blocks++
		}
	}
	println("The answer to part one is " + strconv.Itoa(blocks))
}

type point2D struct {
	x, y int64
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

func renderTiles(tiles map[point2D]int64, score int64) {
	min, max := getBoundingBox(tiles)
	println("Score: " + strconv.FormatInt(score, 10))
	for y := min.y; y <= max.y; y++ {
		line := ""
		for x := min.x; x <= max.x; x++ {
			switch tiles[point2D{x, y}] {
			case 0: // Empty
				line += " "
			case 1: // Wall
				line += "#"
			case 2: // Block
				line += "\u2588"
			case 3: // Paddle
				line += "_"
			case 4: // Ball
				line += "O"
			}
		}
		println(line)
	}
}

func part2(input string) {
	program := intcode.Parse(input)
	program.Memory[0] = 2

	mutex := new(sync.Mutex)
	ballPos := point2D{}
	paddlePos := point2D{}
	// tiles := map[point2D]int64{}
	score := int64(0)

	moves := func() int64 {
		mutex.Lock()
		defer mutex.Unlock()
		// renderTiles(tiles, score)
		if ballPos.x < paddlePos.x {
			return -1 // Left
		} else if ballPos.x > paddlePos.x {
			return 1 // Right
		} else {
			return 0 // Neutral
		}
	}

	gameFeed := program.AsyncRun(moves)
	for x := range gameFeed {
		func() { // defer works at function scope
			mutex.Lock()
			defer mutex.Unlock()
			y := <-gameFeed
			pos := point2D{x, y}
			tile := <-gameFeed
			if x == -1 && y == 0 {
				score = tile
				return
			}
			// tiles[pos] = tile
			switch tile {
			case 3:
				paddlePos = pos
			case 4:
				ballPos = pos
			}
		}()
	}
	println("The answer to part two is " + strconv.FormatInt(score, 10))
}
