package main

import (
	"advent-of-code/aochelpers"
	"math/big"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2019, 22)
	part1(input)
	part2(input)
}

type shuffleRNG struct {
	factor    *big.Int
	increment *big.Int
	modulus   *big.Int
}

func parseShuffle(input string, cardCount *big.Int) shuffleRNG {
	shuffle := shuffleRNG{
		big.NewInt(1),
		big.NewInt(0),
		cardCount,
	}
	for _, line := range strings.Split(input, "\n") {
		if line == "deal into new stack" {
			shuffle.increment.Sub(cardCount, shuffle.increment).Sub(shuffle.increment, big.NewInt(1))
			shuffle.factor.Neg(shuffle.factor)
			continue
		}
		parts := strings.Split(line, " ")
		switch parts[0] {
		case "cut":
			cutOffset, _ := big.NewInt(0).SetString(parts[1], 10)
			shuffle.increment.Add(shuffle.increment, cardCount).Sub(shuffle.increment, cutOffset).Mod(shuffle.increment, cardCount)
		case "deal":
			increment, _ := big.NewInt(0).SetString(parts[3], 10)
			shuffle.factor.Mul(shuffle.factor, increment).Mod(shuffle.factor, cardCount)
			shuffle.increment.Mul(shuffle.increment, increment).Mod(shuffle.increment, cardCount)
		default:
			panic("Unknown shuffle action!")
		}
	}
	for shuffle.factor.Cmp(big.NewInt(0)) < 0 {
		shuffle.factor.Add(shuffle.factor, cardCount)
	}
	return shuffle
}

func (shuffle shuffleRNG) iterate(pos *big.Int) *big.Int {
	return pos.Mul(pos, shuffle.factor).Add(pos, shuffle.increment).Mod(pos, shuffle.modulus)
}

func part1(input string) {
	shuffle := parseShuffle(input, big.NewInt(10007))
	pos := shuffle.iterate(big.NewInt(2019))
	println("The answer to part one is " + pos.String())
}

func part2(input string) {
}
