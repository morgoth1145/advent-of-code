package main

import "advent-of-code/aochelpers"

func main() {
	input := aochelpers.GetInput(2015, 11)
	part1(input)
	part2(input)
}

func inputToPassword(input string) [8]int {
	values := [8]int{}
	for idx, c := range input {
		values[idx] = int(c) - int('a') // a - 0, z - 25
	}
	return values
}

func passwordToString(password [8]int) string {
	chars := []rune{}
	for _, c := range password {
		chars = append(chars, rune(int('a')+c))
	}
	return string(chars)
}

func passwordRule1(password [8]int) bool {
	for idx := 0; idx < len(password)-2; idx++ {
		if password[idx]+1 == password[idx+1] && password[idx]+2 == password[idx+2] {
			return true
		}
	}
	return false
}

func passwordRule2(password [8]int) bool {
	for _, c := range password {
		switch c {
		case 8, 11, 14: // i, l, o
			return false
		}
	}
	return true
}

func passwordRule3(password [8]int) bool {
	var onePair = false
	for idx := 0; idx < len(password)-1; idx++ {
		if password[idx] == password[idx+1] {
			if onePair {
				return true
			}
			onePair = true
			idx++
		}
	}
	return false
}

func incrementPassword(password [8]int) [8]int {
	for idx := 7; idx >= 0; idx-- {
		password[idx]++
		if password[idx] > 25 {
			// Roll over
			password[idx] = 0
			continue
		}
		return password
	}
	return password
}

func getNextPassword(password [8]int) [8]int {
	password = incrementPassword(password)
	for !passwordRule1(password) || !passwordRule2(password) || !passwordRule3(password) {
		password = incrementPassword(password)
	}
	return password
}

func part1(input string) {
	password := inputToPassword(input)
	password = getNextPassword(password)
	println("The answer to part one is " + passwordToString(password))
}

func part2(input string) {
	password := inputToPassword(input)
	password = getNextPassword(password)
	password = getNextPassword(password)
	println("The answer to part two is " + passwordToString(password))
}
