package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 15)
	part1(input)
	part2(input)
}

type ingredientStats struct {
	capacity   int
	durability int
	flavor     int
	texture    int
	calories   int
}

func stripComma(s string) string {
	if s[len(s)-1] == ',' {
		return s[:len(s)-1]
	}
	return s
}

func parse(input string) []ingredientStats {
	ingredients := []ingredientStats{}
	for _, line := range strings.Split(input, "\n") {
		parts := strings.Split(line, " ")
		stats := ingredientStats{}
		stats.capacity, _ = strconv.Atoi(stripComma(parts[2]))
		stats.durability, _ = strconv.Atoi(stripComma(parts[4]))
		stats.flavor, _ = strconv.Atoi(stripComma(parts[6]))
		stats.texture, _ = strconv.Atoi(stripComma(parts[8]))
		stats.calories, _ = strconv.Atoi(parts[10])
		ingredients = append(ingredients, stats)
	}
	return ingredients
}

func generateAmounts(groups int, totalAmount int, handler func([]int)) {
	var generator func([]int, int)
	generator = func(amounts []int, remaining int) {
		if len(amounts) == groups-1 {
			handler(append(amounts, remaining))
			return
		}
		for amount := 0; amount <= remaining; amount++ {
			generator(append(amounts, amount), remaining-amount)
		}
	}
	generator([]int{}, totalAmount)
}

func combine(ingredients []ingredientStats, amounts []int) ingredientStats {
	totalStats := ingredientStats{}
	for idx, amount := range amounts {
		totalStats.capacity += ingredients[idx].capacity * amount
		totalStats.durability += ingredients[idx].durability * amount
		totalStats.flavor += ingredients[idx].flavor * amount
		totalStats.texture += ingredients[idx].texture * amount
		totalStats.calories += ingredients[idx].calories * amount
	}
	return totalStats
}

func scoreIngredients(totalStats ingredientStats) int {
	zeroIfNegative := func(val int) int {
		if val < 0 {
			return 0
		}
		return val
	}
	return zeroIfNegative(totalStats.capacity) * zeroIfNegative(totalStats.durability) * zeroIfNegative(totalStats.flavor) * zeroIfNegative(totalStats.texture)
}

func part1(input string) {
	ingredients := parse(input)
	bestScore := 0
	generateAmounts(len(ingredients), 100, func(amounts []int) {
		score := scoreIngredients(combine(ingredients, amounts))
		if score > bestScore {
			bestScore = score
		}
	})
	println("The answer to part one is " + strconv.Itoa(bestScore))
}

func part2(input string) {
	ingredients := parse(input)
	bestScore := 0
	generateAmounts(len(ingredients), 100, func(amounts []int) {
		totalStats := combine(ingredients, amounts)
		if totalStats.calories != 500 {
			return
		}
		score := scoreIngredients(totalStats)
		if score > bestScore {
			bestScore = score
		}
	})
	println("The answer to part two is " + strconv.Itoa(bestScore))
}
