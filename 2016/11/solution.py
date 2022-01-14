import re

import lib.aoc

def parse_input(s):
    floors = []

    types = []

    for line in s.splitlines():
        generator_flags = 0
        for g in re.findall('[a-zA-Z]+ generator', line):
            g = g.split()[0]
            if g not in types:
                types.append(g)
            generator_flags |= (1 << types.index(g))

        microchip_flags = 0
        for m in re.findall('[a-zA-Z\-]+ microchip', line):
            m = m.split()[0].split('-')[0]
            if m not in types:
                types.append(m)
            microchip_flags |= (1 << types.index(m))

        floors.append((generator_flags, microchip_flags))

    return floors, types

def conflicts(generators, microchips):
    return generators and microchips - (microchips & generators)

def neighbor_states(state):
    elevator, floors = state
    generators, microchips = floors[elevator]

    cand_micros = [1 << idx
                   for idx, c in enumerate(bin(microchips)[2:][::-1])
                   if c == '1']
    cand_gens = [1 << idx
                 for idx, c in enumerate(bin(generators)[2:][::-1])
                 if c == '1']

    neighbor_floors = []
    if elevator > 0:
        neighbor_floors.append(elevator-1)
    if elevator < len(floors)-1:
        neighbor_floors.append(elevator+1)

    for target_floor in neighbor_floors:
        target_gens, target_micros = floors[target_floor]
        for micro_a in cand_micros:
            # Move 2 microchips
            for micro_b in cand_micros:
                if micro_a == micro_b:
                    continue
                left_micros = microchips - micro_a - micro_b
                if conflicts(generators, left_micros):
                    continue
                new_micros = target_micros + micro_a + micro_b
                if conflicts(target_gens, new_micros):
                    continue
                new_floors = list(floors)
                new_floors[elevator] = (generators, left_micros)
                new_floors[target_floor] = (target_gens, new_micros)
                yield target_floor, tuple(new_floors)
            # Move microchip and generator
            for gen_a in cand_gens:
                left_micros = microchips - micro_a
                left_gens = generators - gen_a
                if conflicts(left_gens, left_micros):
                    continue
                new_micros = target_micros + micro_a
                new_gens = target_gens + gen_a
                if conflicts(new_gens, new_micros):
                    continue
                new_floors = list(floors)
                new_floors[elevator] = (left_gens, left_micros)
                new_floors[target_floor] = (new_gens, new_micros)
                yield target_floor, tuple(new_floors)
            # Just move a microchip
            left_micros = microchips - micro_a
            if conflicts(generators, left_micros):
                continue
            new_micros = target_micros + micro_a
            if conflicts(target_gens, new_micros):
                continue
            new_floors = list(floors)
            new_floors[elevator] = (generators, left_micros)
            new_floors[target_floor] = (target_gens, new_micros)
            yield target_floor, tuple(new_floors)
        # Move no microchips
        for gen_a in cand_gens:
            # Move 2 generators
            for gen_b in cand_gens:
                if gen_a == gen_b:
                    continue
                left_gens = generators - gen_a - gen_b
                if conflicts(left_gens, microchips):
                    continue
                new_gens = target_gens + gen_a + gen_b
                if conflicts(new_gens, target_micros):
                    continue
                new_floors = list(floors)
                new_floors[elevator] = (left_gens, microchips)
                new_floors[target_floor] = (new_gens, target_micros)
                yield target_floor, tuple(new_floors)
            # Just move a generator
            left_gens = generators - gen_a
            if conflicts(left_gens, microchips):
                continue
            new_gens = target_gens + gen_a
            if conflicts(new_gens, target_micros):
                continue
            new_floors = list(floors)
            new_floors[elevator] = (left_gens, microchips)
            new_floors[target_floor] = (new_gens, target_micros)
            yield target_floor, tuple(new_floors)

def part1(s):
    floors, types = parse_input(s)

    states = [(0, tuple(floors))]

    seen = set(states)

    steps = 0
    while True:
        steps += 1

        new_states = set()
        for state in states:
            new_states.update(neighbor_states(state))

        done = False
        for _, floors in new_states:
            if all(gens == 0 and micros == 0
                   for gens, micros in floors[:-1]):
                done = True
                break

        if done:
            answer = steps
            break

        new_states -= seen
        seen.update(new_states)

        states = new_states

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 11)
part1(INPUT)
part2(INPUT)
