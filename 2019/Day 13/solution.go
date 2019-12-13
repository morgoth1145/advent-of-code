package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"strconv"
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

func part2(input string) {
}
