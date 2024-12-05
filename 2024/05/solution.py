import lib.aoc

def parse_input(s):
    a, b = s.split('\n\n')

    alist = []
    for l in a.split('\n'):
        alist.append(tuple(map(int, l.split('|'))))

    blist = []
    for l in b.split('\n'):
        blist.append(tuple(map(int, l.split(','))))

    return alist, blist

def part1(s):
    rules, b = parse_input(s)

    answer = 0

    for l in b:
        good = True
        for r0, r1 in rules:
            if r0 in l and r1 in l:
                if l.index(r0) > l.index(r1):
                    good = False
                    break
        if good:
            answer += l[len(l)//2]

    lib.aoc.give_answer(2024, 5, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 5)
part1(INPUT)
part2(INPUT)
