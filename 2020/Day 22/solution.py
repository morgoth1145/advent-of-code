import helpers.input

def iter_game(p1, p2):
    c1, c2 = p1[0], p2[0]
    p1, p2 = p1[1:], p2[1:]
    if c1 > c2:
        p1.append(c1)
        p1.append(c2)
    else:
        p2.append(c2)
        p2.append(c1)
    return p1, p2

def score(deck):
    deck = deck[::-1]
    tot = 0
    for idx, card in enumerate(deck):
        tot += (idx+1) * card
    return tot

def part1(s):
    p1, p2 = s.split('\n\n')
    p1 = list(map(int, p1.splitlines()[1:]))
    p2 = list(map(int, p2.splitlines()[1:]))
    while len(p1) > 0 and len(p2) > 0:
        p1, p2 = iter_game(p1, p2)
    answer = score(p1 + p2)
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 22)

part1(INPUT)
part2(INPUT)
