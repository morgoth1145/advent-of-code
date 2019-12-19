package main

import (
	"advent-of-code/aochelpers"
	"sort"
	"strconv"
	"strings"
	"unicode"
)

func main() {
	input := aochelpers.GetInput(2019, 18)
	part1(input)
	part2(input)
}

type vector2D struct {
	x int
	y int
}

type graphLink struct {
	dest rune
	dist int
}

func surroundingTiles(pos vector2D) []vector2D {
	return []vector2D{
		vector2D{pos.x - 1, pos.y},
		vector2D{pos.x + 1, pos.y},
		vector2D{pos.x, pos.y - 1},
		vector2D{pos.x, pos.y + 1},
	}
}

func parseToGraph(input string) map[rune][]graphLink {
	maze := map[vector2D]rune{}
	features := []vector2D{}
	for y, line := range strings.Split(input, "\n") {
		for x, c := range line {
			pos := vector2D{x, y}
			maze[pos] = c
			if c != '#' && c != '.' {
				features = append(features, pos)
			}
		}
	}
	out := map[rune][]graphLink{}
	for _, startPos := range features {
		links := []graphLink{}
		seen := map[vector2D]bool{}
		steps := -1
		queue := []vector2D{startPos}
		for len(queue) > 0 {
			steps++
			newQueue := []vector2D{}
			for _, pos := range queue {
				{
					_, alreadyHandled := seen[pos]
					if alreadyHandled {
						continue
					}
				}
				seen[pos] = true
				cur := maze[pos]
				if cur == '#' {
					continue
				}
				if cur == '.' || pos == startPos {
					for _, n := range surroundingTiles(pos) {
						newQueue = append(newQueue, n)
					}
					continue
				}
				links = append(links, graphLink{cur, steps})
			}
			queue = newQueue
		}
		out[maze[startPos]] = links
	}
	return out
}

func getMemoKey(curState string, missing map[rune]bool) string {
	rest := []rune{}
	for key := range missing {
		rest = append(rest, key)
	}
	sort.Slice(rest, func(i, j int) bool {
		return rest[i] < rest[j]
	})
	return curState + ":" + string(rest)
}

func getAvailableKeys(start rune, maze map[rune][]graphLink, missing map[rune]bool) map[rune]int {
	out := map[rune]int{}
	bestDistance := map[rune]int{}
	queue := []graphLink{graphLink{start, 0}}
	for len(queue) > 0 {
		item := queue[0]
		queue = queue[1:]
		tile := item.dest
		{
			priorDistance, alreadySeen := bestDistance[tile]
			if alreadySeen && priorDistance <= item.dist {
				continue
			}
			bestDistance[tile] = item.dist
		}
		if unicode.IsUpper(tile) {
			key := unicode.ToLower(tile)
			if missing[key] {
				// The door is locked
				continue
			}
		} else if unicode.IsLower(tile) {
			if missing[tile] {
				// We found a new key!
				out[tile] = item.dist
				continue
			}
		}
		for _, link := range maze[tile] {
			queue = append(queue, graphLink{link.dest, item.dist + link.dist})
		}
		sort.Slice(queue, func(i, j int) bool {
			return queue[i].dist < queue[j].dist
		})
	}
	return out
}

func solve(maze map[rune][]graphLink, start rune) int {
	missing := map[rune]bool{}
	for key := range maze {
		if unicode.IsLower(key) {
			missing[key] = true
		}
	}

	memo := map[string]int{}
	var impl func(rune) int
	impl = func(cur rune) int {
		if 0 == len(missing) {
			return 0
		}
		memoLookup := getMemoKey(string(cur), missing)
		{
			cached, isKnown := memo[memoLookup]
			if isKnown {
				return cached
			}
		}
		best := -1
		for key, dist := range getAvailableKeys(cur, maze, missing) {
			delete(missing, key)
			childBest := impl(key)
			missing[key] = true
			if childBest == -1 {
				continue
			}
			childBest += dist
			if best == -1 || childBest < best {
				best = childBest
			}
		}
		memo[memoLookup] = best
		return best
	}

	return impl(start)
}

func part1(input string) {
	answer := solve(parseToGraph(input), '@')
	println("The answer to part one is " + strconv.Itoa(answer))
}

func part2(input string) {
}
