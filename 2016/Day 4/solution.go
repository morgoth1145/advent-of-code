package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2016, 4)
	part1(input)
	part2(input)
}

type room struct {
	name     string
	sectorID int
	checksum string
}

func parse(input string) []room {
	out := []room{}
	for _, line := range strings.Split(input, "\n") {
		parts := strings.Split(line, "-")
		numberChecksumPart := parts[len(parts)-1]
		name := strings.Join(parts[:len(parts)-1], "-")
		checksumIdx := strings.Index(numberChecksumPart, "[")
		number, _ := strconv.Atoi(numberChecksumPart[:checksumIdx])
		checksum := numberChecksumPart[checksumIdx+1 : len(numberChecksumPart)-1]
		out = append(out, room{name: name, sectorID: number, checksum: checksum})
	}
	return out
}

func getRoomChecksum(name string) string {
	counts := map[rune]int{}
	for _, c := range name {
		if '-' == c {
			continue
		}
		counts[c]++
	}
	out := ""
	for i := 0; i < 5; i++ {
		maxCount := 0
		bestC := 'a'
		for c, num := range counts {
			if num > maxCount {
				maxCount = num
				bestC = c
			} else if num == maxCount && c < bestC {
				bestC = c
			}
		}
		out += string(bestC)
		delete(counts, bestC)
	}
	return out
}

func part1(input string) {
	total := 0
	for _, r := range parse(input) {
		if r.checksum == getRoomChecksum(r.name) {
			total += r.sectorID
		}
	}
	println("The answer to part one is " + strconv.Itoa(total))
}

func decryptName(name string, sectorID int) string {
	shift := sectorID % 26
	out := ""
	for _, c := range name {
		if c == '-' {
			out += " "
		} else {
			c += rune(shift)
			if c > 'z' {
				c -= 26
			}
			out += string(c)
		}
	}
	return out
}

func part2(input string) {
	for _, r := range parse(input) {
		if r.checksum == getRoomChecksum(r.name) && decryptName(r.name, r.sectorID) == "northpole object storage" {
			println("The answer to part two is " + strconv.Itoa(r.sectorID))
			return
		}
	}
}
