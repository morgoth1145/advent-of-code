package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 21)
	part1(input)
	part2(input)
}

type stats struct {
	hp     int
	damage int
	armor  int
}

func parse(input string) stats {
	out := stats{}
	for _, line := range strings.Split(input, "\n") {
		parts := strings.Split(line, " ")
		switch parts[0] {
		case "Hit":
			out.hp, _ = strconv.Atoi(parts[2])
		case "Damage:":
			out.damage, _ = strconv.Atoi(parts[1])
		case "Armor:":
			out.armor, _ = strconv.Atoi(parts[1])
		}
	}
	return out
}

type item struct {
	cost   int
	damage int
	armor  int
}

func getWeapons() []item {
	return []item{
		item{cost: 8, damage: 4, armor: 0},  // Dagger
		item{cost: 10, damage: 5, armor: 0}, // Shortsword
		item{cost: 25, damage: 6, armor: 0}, // Warhammer
		item{cost: 40, damage: 7, armor: 0}, // Longsword
		item{cost: 74, damage: 8, armor: 0}, // Greataxe
	}
}

func getArmor() []item {
	return []item{
		item{cost: 13, damage: 0, armor: 1},  // Leather
		item{cost: 31, damage: 0, armor: 2},  // Chainmail
		item{cost: 53, damage: 0, armor: 3},  // Splintmail
		item{cost: 75, damage: 0, armor: 4},  // Bandedmail
		item{cost: 102, damage: 0, armor: 5}, // Platemail
	}
}

func getRings() []item {
	return []item{
		item{cost: 25, damage: 1, armor: 0},  // Damage +1
		item{cost: 50, damage: 2, armor: 0},  // Damage +2
		item{cost: 100, damage: 3, armor: 0}, // Damage +3
		item{cost: 20, damage: 0, armor: 1},  // Defense +1
		item{cost: 40, damage: 0, armor: 2},  // Defense +2
		item{cost: 80, damage: 0, armor: 3},  // Defense +3
	}
}

func generateLoadouts() [][]item {
	var recursivelyGenerateOptions func([]item, []item, int, func([]item))
	recursivelyGenerateOptions = func(taken []item, choices []item, remainingSlots int, handler func([]item)) {
		if 0 == remainingSlots || 0 == len(choices) {
			handler(taken)
			return
		}
		recursivelyGenerateOptions(taken, choices[1:], remainingSlots, handler)
		recursivelyGenerateOptions(append(append([]item{}, taken...), choices[0]), choices[1:], remainingSlots-1, handler)
	}

	out := [][]item{}
	for _, w := range getWeapons() {
		// Always take 1 weapon
		recursivelyGenerateOptions([]item{}, getArmor(), 1, func(armorChoice []item) {
			recursivelyGenerateOptions([]item{}, getRings(), 2, func(ringsChoice []item) {
				loadout := []item{}
				loadout = append(loadout, w)
				loadout = append(loadout, armorChoice...)
				loadout = append(loadout, ringsChoice...)
				out = append(out, loadout)
			})
		})
	}
	return out
}

func calcActualDamage(damage int, armor int) int {
	adjustedDamage := damage - armor
	if adjustedDamage < 1 {
		adjustedDamage = 1
	}
	return adjustedDamage
}

func doesPlayerWin(boss stats, player stats) bool {
	bossHP := boss.hp
	playerHP := player.hp
	for {
		bossHP -= calcActualDamage(player.damage, boss.armor)
		if bossHP <= 0 {
			return true
		}
		playerHP -= calcActualDamage(boss.damage, player.armor)
		if playerHP <= 0 {
			return false
		}
	}
}

func part1(input string) {
	boss := parse(input)
	best := -1
	for _, loadout := range generateLoadouts() {
		cost := 0
		player := stats{hp: 100}
		for _, i := range loadout {
			cost += i.cost
			player.damage += i.damage
			player.armor += i.armor
			if best == -1 || cost < best {
				if doesPlayerWin(boss, player) {
					best = cost
				}
			}
		}
	}
	println("The answer to part one is " + strconv.Itoa(best))
}

func part2(input string) {
}
