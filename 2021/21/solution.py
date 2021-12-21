import collections
import functools
import itertools

import lib.aoc

def parse_gamestate(s):
    p1, p2 = s.splitlines()

    return int(p1.split()[4]), int(p2.split()[4])

def part1(s):
    p1, p2 = parse_gamestate(s)
    s1, s2 = 0, 0

    die = 1
    rolls = 0

    def play(player):
        nonlocal die
        nonlocal rolls
        rolls += 3
        player = (player + 3 * die + 2) % 10 + 1
        # The board is only 10 long, a 10 sided die and 100 sided die
        # are equivalent for the game
        die = (die + 3) % 10
        return player

    while True:
        p1 = play(p1)
        s1 += p1
        if s1 >= 1000:
            break
        p2 = play(p2)
        s2 += p2
        if s2 >= 1000:
            break

    answer = rolls * min(s1, s2)

    print(f'The answer to part one is {answer}')

def part2(s):
    p1, p2 = parse_gamestate(s)

    # Precompute the moves for *marginally* faster runtime
    QUANTUM_MOVES = collections.Counter(map(sum,
                                            itertools.product((1, 2, 3),
                                                              repeat=3)))

    @functools.cache
    def count_wins(positions, scores, active_player=0):
        positions = list(positions)
        scores = list(scores)
        wins = [0] * len(positions)

        orig_pos = positions[active_player]
        orig_score = scores[active_player]

        for move, universes in QUANTUM_MOVES.items():
            positions[active_player] = (orig_pos + move - 1) % 10 + 1
            scores[active_player] = orig_score + positions[active_player]
            if scores[active_player] >= 21:
                wins[active_player] += universes
            else:
                sub_wins = count_wins(tuple(positions),
                                      tuple(scores),
                                      (active_player+1) % len(positions))
                for idx, count in enumerate(sub_wins):
                    wins[idx] += universes * count

        return wins

    positions = (p1, p2)
    scores = (0, 0)

    answer = max(count_wins(positions, scores))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 21)
part1(INPUT)
part2(INPUT)
