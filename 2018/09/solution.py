import collections

import lib.aoc

def play(players, last_marble):
    scores = [0] * players

    marbles = collections.deque([0])

    player = 0

    for m in range(1, last_marble+1):
        if m % 23 == 0:
            scores[player] += m
            marbles.rotate(7)
            scores[player] += marbles.popleft()
        else:
            marbles.rotate(-2)
            marbles.insert(0, m)

        player = (player + 1) % players

    return scores

def part1(s):
    players, _, _, _, _, _, last_marble, _ = s.split()

    answer = max(play(int(players), int(last_marble)))

    print(f'The answer to part one is {answer}')

def part2(s):
    players, _, _, _, _, _, last_marble, _ = s.split()

    answer = max(play(int(players), 100 * int(last_marble)))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 9)
part1(INPUT)
part2(INPUT)
