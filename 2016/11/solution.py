import collections
import itertools
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

def neighbor_states(state):
    elevator, floors = state
    generators, microchips = floors[elevator]

    # Vectors of things we can move
    move_cands = []

    for idx, c in enumerate(bin(generators)[:1:-1]):
        if c == '1':
            move_cands.append((1 << idx, 0))
    for idx, c in enumerate(bin(microchips)[:1:-1]):
        if c == '1':
            move_cands.append((0, 1 << idx))

    def gen_moves_to_floor(target_floor, items_to_move):
        target_gens, target_micros = floors[target_floor]

        states = []
        for moving in itertools.combinations(move_cands, items_to_move):
            move_gens = 0
            move_micros = 0
            for g, m in moving:
                move_gens += g
                move_micros += m
            left_gens = generators - move_gens
            left_micros = microchips - move_micros
            if left_gens and left_micros - (left_micros & left_gens):
                continue
            new_gens = target_gens + move_gens
            new_micros = target_micros + move_micros
            if new_gens and new_micros - (new_micros & new_gens):
                continue
            new_floors = list(floors)
            new_floors[elevator] = (left_gens, left_micros)
            new_floors[target_floor] = (new_gens, new_micros)
            if elevator == 0 and left_gens == 0 == left_micros:
                # We're moving the last of the items on the ground floor
                # No need to go down here again!
                states.append((0, tuple(new_floors[1:])))
            else:
                states.append((target_floor, tuple(new_floors)))

        return states

    if elevator > 0:
        for items_to_move in (1, 2):
            states = gen_moves_to_floor(elevator-1, items_to_move)
            if states:
                yield from states
                break # Move as little as possible downstairs
    if elevator < len(floors)-1:
        for items_to_move in (2, 1):
            states = gen_moves_to_floor(elevator+1, items_to_move)
            if states:
                yield from states
                break # Move as much as we can upstairs

# Two states are interchangeable if the pairings between floors match up
# It doesn't matter if Generator and Microchip A are on floor 1 or 2
# if Generator and Microchip B are on the other floor! They don't really
# interact beyond stranded microchips being fried by random generators!
def get_state_key(state):
    elevator, floors = state

    pairs = collections.defaultdict(list)

    for idx, (gens, micros) in enumerate(floors):
        for g, c in enumerate(bin(gens)[:1:-1]):
            if c == '1':
                pairs[g].append(idx)
        for m, c in enumerate(bin(micros)[:1:-1]):
            if c == '1':
                pairs[m].append(idx)

    pair_keys = tuple(sorted(((a, b)
                              for a, b in pairs.values())))

    return elevator, len(floors), pair_keys

def min_moves(floors):
    states = [(0, tuple(floors))]

    seen = set(states)

    steps = 0
    while True:
        steps += 1

        new_states = []

        for state in states:
            for new_state in neighbor_states(state):
                if len(new_state[1]) == 1:
                    return steps # Everything is on the top floor!
                key = get_state_key(new_state)
                if key in seen:
                    continue
                seen.add(key)
                new_states.append(new_state)

        states = new_states

def part1(s):
    floors, types = parse_input(s)
    answer = min_moves(floors)

    print(f'The answer to part one is {answer}')

def part2(s):
    floors, types = parse_input(s)

    # Add the extra parts
    elerium_idx = len(types)
    types.append('elerium')
    dilithium_idx = len(types)
    types.append('dilithium')

    add_mask = (1 << elerium_idx) + (1 << dilithium_idx)

    floors = list(floors)
    gens, micros = floors[0]
    floors[0] = (gens + add_mask, micros + add_mask)
    floors = tuple(floors)

    answer = min_moves(floors)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 11)
part1(INPUT)
part2(INPUT)
