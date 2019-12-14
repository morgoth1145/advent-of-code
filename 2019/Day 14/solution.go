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

func part1(input string) {
	reactions := parse(input)
	reactionOrder := getReactionOrder(reactions)
	need := map[string]int64{}
	need["FUEL"] = 1
	for _, item := range reactionOrder {
		needAmnt := need[item]
		r, hasReaction := reactions[item]
		if !hasReaction {
			continue
		}

		times := needAmnt / r.output.amount
		if needAmnt%r.output.amount > 0 {
			times++
		}

		for _, chem := range r.inputs {
			need[chem.name] += times * chem.amount
		}
	}
	println("The answer to part one is " + strconv.FormatInt(need["ORE"], 10))
}

func part2(input string) {
}
