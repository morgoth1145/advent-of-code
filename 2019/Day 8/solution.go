package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 8)
	part1(input)
	part2(input)
}

func splitIntoLayers(input string) []string {
	width := 25
	height := 6
	layerSize := width * height
	out := []string{}
	for len(input) > 0 {
		out = append(out, input[:layerSize])
		input = input[layerSize:]
	}
	return out
}

func part1(input string) {
	bestZeros := len(input)
	bestVal := -1
	for _, layer := range splitIntoLayers(input) {
		zeros := strings.Count(layer, "0")
		if zeros < bestZeros {
			bestZeros = zeros
			bestVal = strings.Count(layer, "1") * strings.Count(layer, "2")
		}
	}
	println("The answer to part one is " + strconv.Itoa(bestVal))
}

func composeLayers(layers []string, layerSize int) string {
	out := ""
	for idx := 0; idx < layerSize; idx++ {
		for _, l := range layers {
			if '0' == l[idx] {
				out += " "
				break
			} else if '1' == l[idx] {
				out += "X"
				break
			}
		}
	}
	return out
}

func part2(input string) {
	width := 25
	height := 6
	composed := composeLayers(splitIntoLayers(input), width*height)
	println("The answer to part two is an image:")
	for len(composed) > 0 {
		println(strings.ReplaceAll(composed[:width], "X", "\u2588"))
		composed = composed[width:]
	}
	println(strings.Repeat("-", width))
}
