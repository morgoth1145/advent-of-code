package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
)

func main() {
	input := aochelpers.GetInput(2015, 22)
	part1(input)
	part2(input)
}

type stats struct {
	hp     int
	damage int
	mana   int
}

type effectTimers struct {
	shield   int
	poison   int
	recharge int
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
		}
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

func bossTurn(onStartTurn func(stats, stats, effectTimers) (stats, stats, effectTimers), boss stats, player stats, effects effectTimers, manaSpent int, best int) int {
	boss, player, effects = onStartTurn(boss, player, effects)
	if player.hp <= 0 {
		return best
	}
	if boss.hp <= 0 {
		return manaSpent
	}
	playerArmor := 0
	if effects.shield > 0 {
		playerArmor = 7
	}
	player.hp -= calcActualDamage(boss.damage, playerArmor)
	if player.hp <= 0 {
		return best
	}
	return playerTurn(onStartTurn, boss, player, effects, manaSpent, best)
}

func magicMissile(onStartTurn func(stats, stats, effectTimers) (stats, stats, effectTimers), boss stats, player stats, effects effectTimers, manaSpent int, best int) int {
	boss.hp -= 4
	player.mana -= 53
	manaSpent += 53
	if best != -1 && best < manaSpent {
		return best
	}
	if boss.hp <= 0 {
		return manaSpent
	}
	return bossTurn(onStartTurn, boss, player, effects, manaSpent, best)
}

func drain(onStartTurn func(stats, stats, effectTimers) (stats, stats, effectTimers), boss stats, player stats, effects effectTimers, manaSpent int, best int) int {
	boss.hp -= 2
	player.hp += 2
	player.mana -= 73
	manaSpent += 73
	if best != -1 && best < manaSpent {
		return best
	}
	if boss.hp <= 0 {
		return manaSpent
	}
	return bossTurn(onStartTurn, boss, player, effects, manaSpent, best)
}

func shield(onStartTurn func(stats, stats, effectTimers) (stats, stats, effectTimers), boss stats, player stats, effects effectTimers, manaSpent int, best int) int {
	if effects.shield > 0 {
		// Cannot cast
		return best
	}
	player.mana -= 113
	effects.shield = 6
	manaSpent += 113
	if best != -1 && best < manaSpent {
		return best
	}
	return bossTurn(onStartTurn, boss, player, effects, manaSpent, best)
}

func poison(onStartTurn func(stats, stats, effectTimers) (stats, stats, effectTimers), boss stats, player stats, effects effectTimers, manaSpent int, best int) int {
	if effects.poison > 0 {
		// Cannot cast
		return best
	}
	player.mana -= 173
	effects.poison = 6
	manaSpent += 173
	if best != -1 && best < manaSpent {
		return best
	}
	return bossTurn(onStartTurn, boss, player, effects, manaSpent, best)
}

func recharge(onStartTurn func(stats, stats, effectTimers) (stats, stats, effectTimers), boss stats, player stats, effects effectTimers, manaSpent int, best int) int {
	if effects.recharge > 0 {
		// Cannot cast
		return best
	}
	player.mana -= 229
	effects.recharge = 5
	manaSpent += 229
	if best != -1 && best < manaSpent {
		return best
	}
	return bossTurn(onStartTurn, boss, player, effects, manaSpent, best)
}

func playerTurn(onStartTurn func(stats, stats, effectTimers) (stats, stats, effectTimers), boss stats, player stats, effects effectTimers, manaSpent int, best int) int {
	boss, player, effects = onStartTurn(boss, player, effects)
	if player.hp <= 0 {
		return best
	}
	if boss.hp <= 0 {
		return manaSpent
	}
	if player.mana < 53 {
		// Cannot cast a spell, lose
		return best
	}
	best = magicMissile(onStartTurn, boss, player, effects, manaSpent, best)
	if player.mana >= 73 {
		best = drain(onStartTurn, boss, player, effects, manaSpent, best)
	}
	if player.mana >= 113 {
		best = shield(onStartTurn, boss, player, effects, manaSpent, best)
	}
	if player.mana >= 173 {
		best = poison(onStartTurn, boss, player, effects, manaSpent, best)
	}
	if player.mana >= 229 {
		best = recharge(onStartTurn, boss, player, effects, manaSpent, best)
	}
	return best
}

func handleEffects(boss stats, player stats, effects effectTimers) (stats, stats, effectTimers) {
	if effects.shield > 0 {
		effects.shield--
	}
	if effects.poison > 0 {
		boss.hp -= 3
		effects.poison--
	}
	if effects.recharge > 0 {
		player.mana += 101
		effects.recharge--
	}
	return boss, player, effects
}

func part1(input string) {
	boss := parse(input)
	player := stats{hp: 50, mana: 500}
	best := playerTurn(handleEffects, boss, player, effectTimers{}, 0, -1)
	println("The answer to part one is " + strconv.Itoa(best))
}

func part2(input string) {
}
