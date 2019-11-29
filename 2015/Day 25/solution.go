package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 25)
	part1(input)
	part2(input)
}

func parse(input string) (int, int) {
	parts := strings.Split(input, " ")
	rowStr := parts[16]
	colStr := parts[18]
	row, _ := strconv.Atoi(rowStr[:len(rowStr)-1])
	col, _ := strconv.Atoi(colStr[:len(colStr)-1])
	return row, col
}

func getCodeIndex(row int, col int) int {
	codeIdx := 0
	for c := 1; c <= col; c++ {
		codeIdx += c
	}
	for r := 1; r < row; r++ {
		codeIdx += col + r - 1
	}
	return codeIdx
}

func getCode(codeIndex int) int64 {
	code := int64(20151125)
	for idx := 1; idx < codeIndex; idx++ {
		code *= 252533
		code = code % 33554393
	}
	return code
}

func part1(input string) {
	row, col := parse(input)
	codeIndex := getCodeIndex(row, col)
	code := getCode(codeIndex)
	println("The answer to part one is " + strconv.FormatInt(code, 10))
}

func part2(input string) {
}
