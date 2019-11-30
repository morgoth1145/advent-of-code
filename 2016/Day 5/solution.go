package main

import (
	"advent-of-code/aochelpers"
	"crypto/md5"
	"fmt"
	"strconv"
)

func main() {
	input := aochelpers.GetInput(2016, 5)
	part1(input)
	part2(input)
}

func getInterestingHash(code string, index int) (string, int) {
	for ; ; index++ {
		hash := fmt.Sprintf("%x", md5.Sum([]byte(code+strconv.Itoa(index))))
		if "00000" == hash[:5] {
			return hash, index
		}
	}
}

func part1(input string) {
	password := ""
	index := 0
	for i := 0; i < 8; i++ {
		hash, newIndex := getInterestingHash(input, index)
		password += string(hash[5])
		index = newIndex + 1
	}
	println("The answer to part one is " + password)
}

func part2(input string) {
	passwordBits := []rune{'_', '_', '_', '_', '_', '_', '_', '_'}
	index := 0
	known := 0
	for known < 8 {
		hash, newIndex := getInterestingHash(input, index)
		index = newIndex + 1
		position := hash[5]
		if position > '7' {
			continue
		}
		idx, _ := strconv.Atoi(string(position))
		value := hash[6]
		if passwordBits[idx] == '_' {
			passwordBits[idx] = rune(value)
			known++
			println("I know more of the password: " + string(passwordBits))
		}
	}
	println("The answer to part two is " + string(passwordBits))
}
