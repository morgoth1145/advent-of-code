package main

import (
	"advent-of-code/aochelpers"
	"crypto/md5"
	"fmt"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 4)
	part1(input)
	part2(input)
}

func part1(input string) {
	for i := 0; ; i++ {
		test := input + strconv.Itoa(i)
		h := md5.New()
		h.Write([]byte(test))
		val := fmt.Sprintf("%x", h.Sum(nil))
		if 0 == strings.Index(val, "00000") {
			println("The answer to part one is " + strconv.Itoa(i))
			return
		}
	}
}

func part2(input string) {
}
