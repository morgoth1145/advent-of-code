import collections
import functools

import lib.aoc

def parse_input(s):
    hp, dmg = s.splitlines()
    return int(hp.split()[2]), int(dmg.split()[1])

Effects = collections.namedtuple('Effects',
                                 ('shield', 'poison', 'recharge', 'hard'))

def iter_effects(boss_hp, mana, effects):
    armor = 0
    if effects.shield:
        armor += 7
        effects = effects._replace(shield=effects.shield-1)
    if effects.poison:
        boss_hp -= 3
        effects = effects._replace(poison=effects.poison-1)
    if effects.recharge:
        mana += 101
        effects = effects._replace(recharge=effects.recharge-1)

    return boss_hp, mana, armor, effects

@functools.cache
def boss_turn(boss_hp, boss_dmg, self_hp, mana, effects):
    boss_hp, mana, armor, effects = iter_effects(boss_hp, mana, effects)

    if boss_hp <= 0:
        return 0

    self_hp -= max(boss_dmg - armor, 1)
    if self_hp <= 0:
        return None

    return player_turn(boss_hp, boss_dmg, self_hp, mana, effects)

@functools.cache
def player_turn(boss_hp, boss_dmg, self_hp, mana, effects):
    if effects.hard:
        self_hp -= 1

    if self_hp <= 0:
        return None

    boss_hp, mana, armor, effects = iter_effects(boss_hp, mana, effects)

    if boss_hp <= 0:
        return 0

    best = None

    if mana >= 53:
        cost = boss_turn(boss_hp-4, boss_dmg, self_hp, mana-53, effects)
        if cost is not None:
            cost += 53
            if best is None or best > cost:
                best = cost

    if mana >= 73:
        cost = boss_turn(boss_hp-2, boss_dmg, self_hp+2, mana-73, effects)
        if cost is not None:
            cost += 73
            if best is None or best > cost:
                best = cost

    if mana >= 113 and not effects.shield:
        cost = boss_turn(boss_hp, boss_dmg, self_hp, mana-113,
                         effects._replace(shield=6))
        if cost is not None:
            cost += 113
            if best is None or best > cost:
                best = cost

    if mana >= 173 and not effects.poison:
        cost = boss_turn(boss_hp, boss_dmg, self_hp, mana-173,
                         effects._replace(poison=6))
        if cost is not None:
            cost += 173
            if best is None or best > cost:
                best = cost

    if mana >= 229 and not effects.recharge:
        cost = boss_turn(boss_hp, boss_dmg, self_hp, mana-229,
                         effects._replace(recharge=5))
        if cost is not None:
            cost += 229
            if best is None or best > cost:
                best = cost

    return best

def part1(s):
    boss_hp, boss_dmg = parse_input(s)

    answer = player_turn(boss_hp, boss_dmg, 50, 500, Effects(0, 0, 0, hard=False))

    print(f'The answer to part one is {answer}')

def part2(s):
    boss_hp, boss_dmg = parse_input(s)

    answer = player_turn(boss_hp, boss_dmg, 50, 500, Effects(0, 0, 0, hard=True))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 22)
part1(INPUT)
part2(INPUT)
