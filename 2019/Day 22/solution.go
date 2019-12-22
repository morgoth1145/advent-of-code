package main

import (
	"advent-of-code/aochelpers"
	"advent-of-code/helpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 22)
	part1(input)
	part2(input)
}

func cut(deck []int, offset int) []int {
	if offset < 0 {
		offset += len(deck)
	}
	newDeck := []int{}
	newDeck = append(newDeck, deck[offset:]...)
	newDeck = append(newDeck, deck[:offset]...)
	return newDeck
}

func dealIncrement(deck []int, increment int) []int {
	newDeck := make([]int, len(deck))
	idx := 0
	for _, card := range deck {
		newDeck[idx] = card
		idx += increment
		idx = idx % len(deck)
	}
	return newDeck
}

func part1(input string) {
	cardCount := 10007
	deck := []int{}
	for len(deck) < cardCount {
		deck = append(deck, len(deck))
	}
	for _, line := range strings.Split(input, "\n") {
		if line == "deal into new stack" {
			deck = helpers.ReverseInts(deck)
			continue
		}
		parts := strings.Split(line, " ")
		switch parts[0] {
		case "cut":
			offset, _ := strconv.Atoi(parts[1])
			deck = cut(deck, offset)
		case "deal":
			increment, _ := strconv.Atoi(parts[3])
			deck = dealIncrement(deck, increment)
		default:
			panic("Unknown shuffle action!")
		}
	}
	for idx, card := range deck {
		if card == 2019 {
			println("The answer to part one is " + strconv.Itoa(idx))
			return
		}
	}
	panic("Card 2019 not found!")
}

func part2(input string) {
}
