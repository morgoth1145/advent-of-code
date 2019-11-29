package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 7)
	part1(input)
	part2(input)
}

type command struct {
	output string
	action string
	in1    string
	in2    string
}

func parseCommands(input string) ([]command, map[string]uint16) {
	lines := strings.Split(input, "\n")
	commands := []command{}
	initialValues := map[string]uint16{}
	for _, s := range lines {
		cmd := command{}
		parts := strings.Split(s, " -> ")
		cmd.output = parts[1]
		parts = strings.Split(parts[0], " ")
		if 1 == len(parts) {
			cmd.action = "STORE"
			cmd.in1 = parts[0]
			value, error := strconv.ParseUint(cmd.in1, 10, 16)
			if error == nil {
				initialValues[cmd.output] = uint16(value)
				continue
			}
		} else if "NOT" == parts[0] {
			cmd.action = "NOT"
			cmd.in1 = parts[1]
		} else {
			cmd.in1 = parts[0]
			cmd.action = parts[1]
			cmd.in2 = parts[2]
		}
		commands = append(commands, cmd)
	}
	return commands, initialValues
}

func topologicalSort(dependencyMap map[string][]string) []string {
	seen := make(map[string]bool)
	output := []string{}
	var recursiveSort func(string)
	recursiveSort = func(item string) {
		{
			_, alreadyHandled := seen[item]
			if alreadyHandled {
				return
			}
		}
		seen[item] = true
		dependencies, _ := dependencyMap[item]
		for _, dep := range dependencies {
			recursiveSort(dep)
		}
		output = append(output, item)
	}
	for key := range dependencyMap {
		recursiveSort(key)
	}
	return output
}

func topologicalSortCommands(commands []command) []command {
	wireMap := make(map[string]command)
	dependencyMap := make(map[string][]string)
	for _, cmd := range commands {
		wireMap[cmd.output] = cmd
		dependencies := []string{cmd.in1}
		if len(cmd.in2) > 0 {
			dependencies = append(dependencies, cmd.in2)
		}
		dependencyMap[cmd.output] = dependencies
	}
	output := []command{}
	for _, key := range topologicalSort(dependencyMap) {
		cmd, present := wireMap[key]
		if present {
			output = append(output, cmd)
		}
	}
	return output
}

func getValue(wires map[string]uint16, input string) uint16 {
	value, err := strconv.ParseUint(input, 10, 16)
	if err == nil {
		return uint16(value)
	}
	return wires[input]
}

func executeCommands(wires map[string]uint16, commands []command) {
	for _, cmd := range commands {
		var value uint16
		switch cmd.action {
		case "STORE":
			value = getValue(wires, cmd.in1)
			break
		case "NOT":
			value = ^getValue(wires, cmd.in1)
			break
		case "LSHIFT":
			value = getValue(wires, cmd.in1) << getValue(wires, cmd.in2)
			break
		case "RSHIFT":
			value = getValue(wires, cmd.in1) >> getValue(wires, cmd.in2)
			break
		case "AND":
			value = getValue(wires, cmd.in1) & getValue(wires, cmd.in2)
			break
		case "OR":
			value = getValue(wires, cmd.in1) | getValue(wires, cmd.in2)
			break
		}
		wires[cmd.output] = value
	}
}

func part1(input string) {
	commands, wires := parseCommands(input)
	commands = topologicalSortCommands(commands)
	executeCommands(wires, commands)
	println("The answer to part one is " + strconv.Itoa(int(wires["a"])))
}

func part2(input string) {
	commands, wires := parseCommands(input)
	commands = topologicalSortCommands(commands)
	executeCommands(wires, commands)
	wires = map[string]uint16{"b": wires["a"]}
	executeCommands(wires, commands)
	println("The answer to part two is " + strconv.Itoa(int(wires["a"])))
}