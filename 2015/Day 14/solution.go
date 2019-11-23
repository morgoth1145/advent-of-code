package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 14)
	part1(input)
	part2(input)
}

type reindeerStats struct {
	speed      int
	flightTime int
	restTime   int
}

func parse(input string) []reindeerStats {
	reindeer := []reindeerStats{}
	for _, line := range strings.Split(input, "\n") {
		parts := strings.Split(line, " ")
		stats := reindeerStats{}
		stats.speed, _ = strconv.Atoi(parts[3])
		stats.flightTime, _ = strconv.Atoi(parts[6])
		stats.restTime, _ = strconv.Atoi(parts[13])
		reindeer = append(reindeer, stats)
	}
	return reindeer
}

func calcDistance(stats reindeerStats, time int) int {
	cycleTime := stats.flightTime + stats.restTime
	fullCycles := time / cycleTime
	time = time % cycleTime
	lastCycleFlightTime := stats.flightTime
	if lastCycleFlightTime > time {
		lastCycleFlightTime = time
	}
	return stats.speed * (fullCycles*stats.flightTime + lastCycleFlightTime)
}

func part1(input string) {
	reindeer := parse(input)
	bestDistance := 0
	for _, stats := range reindeer {
		distance := calcDistance(stats, 2503)
		if distance > bestDistance {
			bestDistance = distance
		}
	}
	println("The answer to part one is " + strconv.Itoa(bestDistance))
}

func part2(input string) {
	reindeer := parse(input)
	scores := map[int]int{}
	for time := 1; time <= 2503; time++ {
		bestDistance := 0
		bestIndices := []int{}
		for idx, stats := range reindeer {
			distance := calcDistance(stats, time)
			if distance > bestDistance {
				bestDistance = distance
				bestIndices = []int{idx}
			} else if distance == bestDistance {
				bestIndices = append(bestIndices, idx)
			}
		}
		for _, bestIdx := range bestIndices {
			scores[bestIdx]++
		}
	}
	bestScore := 0
	for _, score := range scores {
		if score > bestScore {
			bestScore = score
		}
	}
	println("The answer to part one is " + strconv.Itoa(bestScore))
}
