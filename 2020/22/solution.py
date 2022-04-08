import lib.aoc

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
    lib.aoc.give_answer(2020, 22, 1, answer)

def play_recursive(p1, p2):
    seen = set()
    while len(p1) > 0 and len(p2) > 0:
        state = (tuple(p1), tuple(p2))
        if state in seen:
            # Player 1 wins!
            return p1, []
        seen.add(state)
        c1, c2 = p1[0], p2[0]
        p1, p2 = p1[1:], p2[1:]
        if len(p1) >= c1 and len(p2) >= c2:
            win1, win2 = play_recursive(list(p1[:c1]), list(p2[:c2]))
            if win1:
                p1.append(c1)
                p1.append(c2)
            else:
                p2.append(c2)
                p2.append(c1)
            continue
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
    return p1, p2

def part2(s):
    p1, p2 = s.split('\n\n')
    p1 = list(map(int, p1.splitlines()[1:]))
    p2 = list(map(int, p2.splitlines()[1:]))
    p1, p2 = play_recursive(p1, p2)
    answer = score(p1 + p2)
    lib.aoc.give_answer(2020, 22, 2, answer)

INPUT = lib.aoc.get_input(2020, 22)

part1(INPUT)
part2(INPUT)
