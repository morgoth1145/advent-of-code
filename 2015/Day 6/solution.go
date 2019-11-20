package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 6)
	part1(input)
	part2(input)
}

type command struct {
	action string
	top    int
	left   int
	bottom int
	right  int
}

func parseCommands(input string) []command {
	lines := strings.Split(input, "\n")
	out := []command{}
	for _, s := range lines {
		cmd := command{}
		parts := strings.Split(s, " ")
		var c1 string
		var c2 string
		if "toggle" == parts[0] {
			cmd.action = parts[0]
			c1 = parts[1]
			c2 = parts[3]
		} else {
			cmd.action = parts[1]
			c1 = parts[2]
			c2 = parts[4]
		}
		leftTop := strings.Split(c1, ",")
		rightBottom := strings.Split(c2, ",")
		cmd.top, _ = strconv.Atoi(leftTop[1])
		cmd.left, _ = strconv.Atoi(leftTop[0])
		cmd.bottom, _ = strconv.Atoi(rightBottom[1])
		cmd.right, _ = strconv.Atoi(rightBottom[0])
		out = append(out, cmd)
	}
	return out
}

func part1(input string) {
	grid := [1000][1000]bool{}
	for _, cmd := range parseCommands(input) {
		for x := cmd.left; x <= cmd.right; x++ {
			for y := cmd.top; y <= cmd.bottom; y++ {
				if "on" == cmd.action {
					grid[x][y] = true
				} else if "off" == cmd.action {
					grid[x][y] = false
				} else if "toggle" == cmd.action {
					grid[x][y] = !grid[x][y]
				}
			}
		}
	}
	count := 0
	for x := 0; x < 1000; x++ {
		for y := 0; y < 1000; y++ {
			if grid[x][y] {
				count++
			}
		}
	}
	println("The answer to part one is " + strconv.Itoa(count))
}

func part2(input string) {
}
