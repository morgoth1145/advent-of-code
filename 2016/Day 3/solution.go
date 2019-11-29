package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2016, 3)
	part1(input)
	part2(input)
}

type polysides struct {
	a int
	b int
	c int
}

func parse(input string) []polysides {
	out := []polysides{}
	for _, line := range strings.Split(input, "\n") {
		parts := strings.Fields(line)
		if len(parts) != 3 {
			panic("Bad!")
		}
		a, _ := strconv.Atoi(parts[0])
		b, _ := strconv.Atoi(parts[1])
		c, _ := strconv.Atoi(parts[2])
		out = append(out, polysides{a, b, c})
	}
	return out
}

func countPossibleTriangles(triangles []polysides) int {
	count := 0
	for _, tri := range triangles {
		sum := tri.a + tri.b + tri.c
		if sum > 2*tri.a && sum > 2*tri.b && sum > 2*tri.c {
			count++
		}
	}
	return count
}

func part1(input string) {
	println("The answer to part one is " + strconv.Itoa(countPossibleTriangles(parse(input))))
}

func fixTriangles(triangles []polysides) []polysides {
	out := []polysides{}
	for idx := 0; idx < len(triangles); idx += 3 {
		out = append(out, polysides{triangles[idx].a, triangles[idx+1].a, triangles[idx+2].a})
		out = append(out, polysides{triangles[idx].b, triangles[idx+1].b, triangles[idx+2].b})
		out = append(out, polysides{triangles[idx].c, triangles[idx+1].c, triangles[idx+2].c})
	}
	return out
}

func part2(input string) {
	println("The answer to part one is " + strconv.Itoa(countPossibleTriangles(fixTriangles(parse(input)))))
}
