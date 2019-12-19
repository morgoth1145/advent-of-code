package main

import (
	"advent-of-code/2019/channeltypes"
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2019, 19)
	part1(input)
	part2(input)
}

func isSquareAffected(x int, y int, program intcode.Program) bool {
	coordInputs := channeltypes.List(int64(x), int64(y))
	affected := program.Clone().AsyncRun(intcode.InputChannelFunction(coordInputs, intcode.EOFPanic))
	if 1 == <-affected {
		return true
	}
	return false
}

func part1(input string) {
	program := intcode.Parse(input)
	totalAffected := 0
	for x := 0; x < 50; x++ {
		for y := 0; y < 50; y++ {
			if isSquareAffected(x, y, program) {
				totalAffected++
			}
		}
	}
	println("The answer to part one is " + strconv.Itoa(totalAffected))
}

func part2(input string) {
	program := intcode.Parse(input)
	startX := 0
	for y := 50; ; y++ {
		for x := startX; ; x++ {
			if !isSquareAffected(x, y, program) {
				continue
			}
			startX = x
			candidateBlockX := startX
			candidateBlockY := y - 99
			shouldTest := false
			{
				if isSquareAffected(candidateBlockX+99, candidateBlockY, program) {
					shouldTest = true
				}
			}
			if shouldTest {
				isGood := true
				for testX := candidateBlockX; testX < candidateBlockX+100; testX++ {
					for testY := candidateBlockY; testY < candidateBlockY+100; testY++ {
						if !isSquareAffected(testX, testY, program) {
							isGood = false
							break
						}
					}
					if !isGood {
						break
					}
				}
				if isGood {
					println("The answer to part two is " + strconv.Itoa(candidateBlockX*10000+candidateBlockY))
					return
				}
			}
			break
		}
	}
}
