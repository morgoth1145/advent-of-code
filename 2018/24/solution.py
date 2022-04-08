import lib.aoc

class Group:
    def __init__(self, count, hp, dmg, dmg_type, init, weaknesses, immunities):
        self.count = count
        self.hp = hp
        self.dmg = dmg
        self.dmg_type = dmg_type
        self.init = init
        self.weaknesses = weaknesses
        self.immunities = immunities

    @property
    def effective_power(self):
        return self.count * self.dmg

    def computed_dmg(self, enemy_group):
        if self.dmg_type in enemy_group.immunities:
            return 0

        if self.dmg_type in enemy_group.weaknesses:
            return self.effective_power * 2

        return self.effective_power

    def take_damage(self, damage):
        units_killed = damage // self.hp
        self.count = max(0, self.count - units_killed)

def parse_units(s):
    _, *units = s.splitlines()

    for line in units:
        weaknesses = set()
        immunities = set()

        idx = line.find('(')
        if idx != -1:
            idx2 = line.find(')')
            specials = line[idx+1:idx2]
            line = line[:idx] + line[idx2+1:]

            for part in specials.split('; '):
                t, _, *dmg_types = part.split()
                dmg_types = [dt.rstrip(',') for dt in dmg_types]
                if t == 'weak':
                    weaknesses.update(dmg_types)
                if t == 'immune':
                    immunities.update(dmg_types)

        parts = line.split()

        count = int(parts[0])
        hp = int(parts[4])
        dmg = int(parts[12])
        dmg_type = parts[13]
        init = int(parts[17])

        yield Group(count, hp, dmg, dmg_type, init, weaknesses, immunities)

def fight(immune, infection):
    forces = [immune, infection]

    target_order = []

    for force_idx, force in enumerate(forces):
        for group_idx, group in enumerate(force):
            target_order.append((group.effective_power,
                                 group.init,
                                 force_idx,
                                 group_idx))

    target_order.sort(reverse=True)

    targets = {}
    defending = set()

    for _, _, force_idx, group_idx in target_order:
        group = forces[force_idx][group_idx]

        enemy_force = 1 - force_idx
        candidates = []
        for enemy_group_idx, enemy_group in enumerate(forces[enemy_force]):
            if (enemy_force, enemy_group_idx) in defending:
                continue

            computed_dmg = group.computed_dmg(enemy_group)
            if computed_dmg == 0:
                continue

            candidates.append((computed_dmg,
                               enemy_group.effective_power,
                               enemy_group.init,
                               enemy_group_idx))

        if len(candidates) == 0:
            continue

        candidates.sort(reverse=True)

        enemy_group_idx = candidates[0][-1]
        targets[force_idx, group_idx] = enemy_group_idx
        defending.add((enemy_force, enemy_group_idx))

    attack_order = []

    for force_idx, force in enumerate(forces):
        for group_idx, group in enumerate(force):
            attack_order.append((group.init,
                                 force_idx,
                                 group_idx))

    attack_order.sort(reverse=True)

    for _, force_idx, group_idx in attack_order:
        if (force_idx, group_idx) not in targets:
            continue

        group = forces[force_idx][group_idx]
        if group.count == 0:
            # Wiped out!
            continue

        enemy_force = 1 - force_idx
        enemy_group_idx = targets[force_idx, group_idx]

        enemy_group = forces[enemy_force][enemy_group_idx]
        enemy_group.take_damage(group.computed_dmg(enemy_group))

    immune, infection = forces
    immune = [group for group in immune
              if group.count > 0]
    infection = [group for group in infection
                 if group.count > 0]

    return immune, infection

def fight_to_the_death(s, boost=0):
    immune, infection = s.split('\n\n')

    immune = list(parse_units(immune))
    infection = list(parse_units(infection))

    for group in immune:
        group.dmg += boost

    while len(immune) > 0 and len(infection) > 0:
        imm_counts = [g.count for g in immune]
        inf_counts = [g.count for g in infection]
        immune, infection = fight(immune, infection)
        if ([g.count for g in immune] == imm_counts and
            [g.count for g in infection] == inf_counts):
            # Stalemate
            return None, None

    return immune, infection

def part1(s):
    immune, infection = fight_to_the_death(s)

    answer = sum(group.count for group in immune + infection)

    lib.aoc.give_answer(2018, 24, 1, answer)

def part2(s):
    min_boost = 0
    while True:
        min_boost += 1

        immune, infection = fight_to_the_death(s, min_boost)
        if immune is None:
            continue

        if len(infection) == 0:
            break

    immune, infection = fight_to_the_death(s, min_boost)
    assert(len(infection) == 0)

    answer = sum(group.count for group in immune + infection)

    lib.aoc.give_answer(2018, 24, 2, answer)

INPUT = lib.aoc.get_input(2018, 24)
part1(INPUT)
part2(INPUT)
