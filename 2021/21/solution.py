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
    pass

INPUT = lib.aoc.get_input(2021, 21)
part1(INPUT)
part2(INPUT)
