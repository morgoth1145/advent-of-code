import itertools

import lib.aoc

def parse_input(s):
    hp, dmg, armor = s.splitlines()
    return int(hp.split()[2]), int(dmg.split()[1]), int(armor.split()[1])

# Cost, Damage, Armor
WEAPONS = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
]
ARMOR = [
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]
RINGS = [
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]

def item_combos():
    for weapon in itertools.combinations(WEAPONS, 1):
        for armor_count in range(2):
            for armor in itertools.combinations(ARMOR, armor_count):
                for ring_count in range(3):
                    for rings in itertools.combinations(RINGS, ring_count):
                        items = weapon + armor + rings

                        cost, dmg, arm = 0, 0, 0

                        for c, d, a in items:
                            cost += c
                            dmg += d
                            arm += a

                        yield cost, dmg, arm

def can_win(boss_stats, player_stats):
    boss_hp, boss_damage, boss_armor = boss_stats
    player_hp, player_damage, player_armor = player_stats

    player_real_damage = max(player_damage - boss_armor, 1)
    boss_real_damage = max(boss_damage - player_armor, 1)

    player_attacks_to_win = boss_hp // player_real_damage
    if boss_hp % player_real_damage > 0:
        player_attacks_to_win += 1

    boss_attacks_to_win = player_hp // boss_real_damage
    if player_hp % boss_real_damage > 0:
        boss_attacks_to_win += 1

    return player_attacks_to_win <= boss_attacks_to_win

def part1(s):
    boss_stats = parse_input(s)

    for cost, damage, armor in sorted(item_combos()):
        if can_win(boss_stats, (100, damage, armor)):
            answer = cost
            break

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 21)
part1(INPUT)
part2(INPUT)
