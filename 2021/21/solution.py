import functools

import lib.aoc

def parse_input(s):
    p1, p2 = s.splitlines()
    p1 = int(p1.split()[4])
    p2 = int(p2.split()[4])

    return p1, p2

def gen_die():
    while True:
        for n in range(1, 101):
            yield n

def step(player, score, die):
    r1 = next(die)
    r2 = next(die)
    r3 = next(die)
    player += r1 + r2 + r3
    while player > 10:
        player -= 10
    score += player

    return player, score

def part1(s):
    p1, p2 = parse_input(s)
    s1, s2 = 0, 0

    die = gen_die()

    rolls = 0

    while True:
        p1, s1 = step(p1, s1, die)
        rolls += 3
        if s1 >= 1000:
            break
        p2, s2 = step(p2, s2, die)
        rolls += 3
        if s2 >= 1000:
            break

    answer = rolls * min(s1, s2)

    print(f'The answer to part one is {answer}')

def part2(s):
    p1, p2 = parse_input(s)

    @functools.cache
    def impl(p1, p2, s1=0, s2=0, active_player=1):
        p1_wins = 0
        p2_wins = 0
        for r1 in (1, 2, 3):
            for r2 in (1, 2, 3):
                for r3 in (1, 2, 3):
                    if active_player == 1:
                        new_p1 = p1 + r1 + r2 + r3
                        while new_p1 > 10:
                            new_p1 -= 10
                        new_s1 = s1 + new_p1
                        if new_s1 >= 21:
                            p1_wins += 1
                        else:
                            sub_p1_wins, sub_p2_wins = impl(new_p1, p2, new_s1, s2, 2)
                            p1_wins += sub_p1_wins
                            p2_wins += sub_p2_wins
                    else:
                        new_p2 = p2 + r1 + r2 + r3
                        while new_p2 > 10:
                            new_p2 -= 10
                        new_s2 = s2 + new_p2
                        if new_s2 >= 21:
                            p2_wins += 1
                        else:
                            sub_p1_wins, sub_p2_wins = impl(p1, new_p2, s1, new_s2, 1)
                            p1_wins += sub_p1_wins
                            p2_wins += sub_p2_wins
        return p1_wins, p2_wins

    p1_wins, p2_wins = impl(p1, p2)

    answer = max(p1_wins, p2_wins)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 21)
part1(INPUT)
part2(INPUT)
