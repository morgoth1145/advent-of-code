package main

import (
	"advent-of-code/aochelpers"
	"advent-of-code/helpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 14)
	part1(input)
	part2(input)
}

type chemicalPart struct {
	amount int64
	name   string
}

type reaction struct {
	inputs []chemicalPart
	output chemicalPart
}

func parse(input string) map[string]reaction {
	parseChemical := func(chem string) chemicalPart {
		parts := strings.Split(chem, " ")
		amount, _ := strconv.Atoi(parts[0])
		return chemicalPart{int64(amount), parts[1]}
	}
	out := map[string]reaction{}
	for _, line := range strings.Split(input, "\n") {
		parts := strings.Split(line, " => ")
		inputs := []chemicalPart{}
		for _, item := range strings.Split(parts[0], ", ") {
			inputs = append(inputs, parseChemical(item))
		}
		output := parseChemical(parts[1])
		out[output.name] = reaction{inputs, output}
	}
	return out
}

func getReactionOrder(reactions map[string]reaction) []string {
	graph := map[string][]string{}
	for _, r := range reactions {
		inputs := []string{}
		for _, i := range r.inputs {
			inputs = append(inputs, i.name)
		}
		graph[r.output.name] = inputs
	}
	return helpers.ReverseStrings(helpers.TopologicalSortStrings(graph))
}

func makeFuel(reactions map[string]reaction, amounts map[string]int64, desiredFuel int64) map[string]int64 {
	reactionOrder := getReactionOrder(reactions)
	storedFuel := amounts["FUEL"]
	amounts["FUEL"] = -desiredFuel
	for _, item := range reactionOrder {
		needAmnt := -amounts[item]
		if needAmnt <= 0 {
			continue
		}
		r, hasReaction := reactions[item]
		if !hasReaction {
			continue
		}

		times := needAmnt / r.output.amount
		if needAmnt%r.output.amount > 0 {
			times++
		}

		amounts[r.output.name] += times * r.output.amount
		for _, chem := range r.inputs {
			amounts[chem.name] -= times * chem.amount
		}
	}
	amounts["FUEL"] += storedFuel + desiredFuel
	return amounts
}

func part1(input string) {
	reactions := parse(input)
	amounts := makeFuel(reactions, map[string]int64{}, 1)
	println("The answer to part one is " + strconv.FormatInt(-amounts["ORE"], 10))
}

func part2(input string) {
	reactions := parse(input)
	jumpSize := -makeFuel(reactions, map[string]int64{}, 1)["ORE"]

	oreBank := int64(1000000000000)
	amounts := map[string]int64{"ORE": oreBank}
	best := int64(0)
	for amounts["ORE"] > 0 {
		best = amounts["FUEL"]
		toMake := amounts["ORE"] / jumpSize
		if toMake == 0 {
			toMake++
		}
		amounts = makeFuel(reactions, amounts, toMake)
	}
	println("The answer to part two is " + strconv.FormatInt(best, 10))
}
