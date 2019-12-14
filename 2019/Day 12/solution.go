package main

import (
	"advent-of-code/aochelpers"
	"advent-of-code/helpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 12)
	part1(input)
	part2(input)
}

type moonAxis struct {
	pos []int
	vel []int
}
type moons struct {
	x moonAxis
	y moonAxis
	z moonAxis
}

func parse(input string) moons {
	out := moons{}
	for _, line := range strings.Split(input, "\n") {
		line = strings.Trim(line, "<")
		line = strings.Trim(line, ">")
		for _, part := range strings.Split(line, ", ") {
			subparts := strings.Split(part, "=")
			val, _ := strconv.Atoi(subparts[1])
			switch subparts[0] {
			case "x":
				out.x.pos = append(out.x.pos, val)
				out.x.vel = append(out.x.vel, 0)
			case "y":
				out.y.pos = append(out.y.pos, val)
				out.y.vel = append(out.y.vel, 0)
			case "z":
				out.z.pos = append(out.z.pos, val)
				out.z.vel = append(out.z.vel, 0)
			}
		}
	}
	return out
}

func updateAxis(axis moonAxis) moonAxis {
	for i := 0; i < len(axis.pos); i++ {
		for j := i + 1; j < len(axis.pos); j++ {
			if axis.pos[i] > axis.pos[j] {
				axis.vel[i]--
				axis.vel[j]++
			} else if axis.pos[i] < axis.pos[j] {
				axis.vel[i]++
				axis.vel[j]--
			}
		}
	}
	for i := 0; i < len(axis.pos); i++ {
		axis.pos[i] += axis.vel[i]
	}
	return axis
}

func updateMoons(m moons) moons {
	m.x = updateAxis(m.x)
	m.y = updateAxis(m.y)
	m.z = updateAxis(m.z)
	return m
}

func calcEnergy(m moons) int {
	totalEnergy := 0
	for i := 0; i < len(m.x.pos); i++ {
		totalEnergy += (helpers.Abs(m.x.pos[i]) + helpers.Abs(m.y.pos[i]) + helpers.Abs(m.z.pos[i])) *
			(helpers.Abs(m.x.vel[i]) + helpers.Abs(m.y.vel[i]) + helpers.Abs(m.z.vel[i]))
	}
	return totalEnergy
}

func part1(input string) {
	moons := parse(input)
	for iter := 0; iter < 1000; iter++ {
		moons = updateMoons(moons)
	}
	println("The answer to part one is " + strconv.Itoa(calcEnergy(moons)))
}

func getCycleLength(axis moonAxis) int64 {
	axisString := func() string {
		out := ""
		for _, v := range axis.pos {
			out += strconv.Itoa(v) + " "
		}
		for _, v := range axis.vel {
			out += strconv.Itoa(v) + " "
		}
		return out
	}
	start := axisString()
	for iter := int64(1); true; iter++ {
		axis = updateAxis(axis)
		if axisString() == start {
			return iter
		}
	}
	return -1
}

func part2(input string) {
	moons := parse(input)
	println("The answer to part two is " + strconv.FormatInt(helpers.LCM64(getCycleLength(moons.x), getCycleLength(moons.y), getCycleLength(moons.z)), 10))
}
