package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
)

func main() {
	input := aochelpers.GetInput(2019, 25)
	part1(input)
	part2(input)
}

func part1(input string) {
	// TODO: Write a program to automatically explore the maze, test things, and find the solution
	// I got this input manually. Yes, this *is* a game, but this is also Advent of Code!
	// TODO: Also figure out a better way to start up go programs with input.
	optimalSequence := `west
take mouse
north
west
north
north
west
north
take wreath
south
east
south
east
take hypercube
north
east
take prime number
west
south
west
south
west
west
north
`
	// inputChan := make(chan int64, 100)
	inputChan := make(chan int64)
	go func() {
		for _, c := range optimalSequence {
			inputChan <- int64(c)
		}
	}()
	outputChan := intcode.Parse(input).AsyncRun(intcode.InputChannelFunction(inputChan, intcode.EOFTerminateProgram))
	last := ""
	for c := range outputChan {
		if c == '\n' {
			println(last)
			// if last == "Command?\n" {
			// 	reader := bufio.NewReader(os.Stdin)
			// 	text, _ := reader.ReadString('\n')
			// 	text = strings.ReplaceAll(text, "\r", "")
			// 	for _, inputC := range text {
			// 		inputChan <- int64(inputC)
			// 	}
			// }
			last = ""
		} else {
			last += string(rune(c))
		}
	}
}

func takeComboString(items []string, mask int) string {
	if 0 == len(items) {
		return ""
	}
	out := ""
	if 1 == mask&1 {
		out += "take " + items[0] + "\n"
	}
	return out + takeComboString(items[1:], mask>>1)
}

func dropComboString(items []string, mask int) string {
	if 0 == len(items) {
		return ""
	}
	out := ""
	if 1 == mask&1 {
		out += "drop " + items[0] + "\n"
	}
	return out + dropComboString(items[1:], mask>>1)
}

func part2(input string) {
	pathGatherAndDropItems := `north
take astronaut ice cream
south
west
take mouse
north
take ornament
west
north
take easter egg
north
west
north
take wreath
south
east
south
east
take hypercube
north
east
take prime number
west
south
west
south
west
take mug
west
drop ornament
drop hypercube
drop mug
drop prime number
drop astronaut ice cream
drop mouse
drop wreath
drop easter egg
`
	comboAttempts := ""
	items := []string{
		"ornament",
		"hypercube",
		"mug",
		"prime number",
		"astronaut ice cream",
		"mouse",
		"wreath",
		"easter egg",
	}
	for combo := 0; combo < 256; combo++ {
		comboAttempts += takeComboString(items, combo) + "north\n" + dropComboString(items, combo)
	}
	inputChan := make(chan int64, len(pathGatherAndDropItems)+len(comboAttempts))
	go func() {
		for _, c := range pathGatherAndDropItems + comboAttempts {
			inputChan <- int64(c)
		}
	}()
	outputChan := intcode.Parse(input).AsyncRun(intcode.InputChannelFunction(inputChan, intcode.EOFTerminateProgram))
	last := ""
	line := ""
	for c := range outputChan {
		if c == '\n' {
			println(line)
			last, line = line, ""
		} else {
			line += string(rune(c))
		}
	}
	println(last)
}
