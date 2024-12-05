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

def verify(rules, l):
    for r0, r1 in rules:
        if r0 in l and r1 in l:
            if l.index(r0) > l.index(r1):
                return False
    return True

def part1(s):
    rules, b = parse_input(s)

    answer = 0

    for l in b:
        if verify(rules, l):
            answer += l[len(l)//2]

    lib.aoc.give_answer(2024, 5, 1, answer)

def reorder(rules, l):
    g = {}
    for a, b in rules:
        key = tuple(sorted([a, b]))
        g[key] = (a, b)

    new_l = []

    for item in l:
        placed = False
        for i, other in enumerate(new_l):
            key = tuple(sorted([item, other]))
            if key in g:
                if g[key] == (item, other):
                    new_l.insert(i, item)
                    placed = True
                    break
        if not placed:
            new_l.append(item)

    return new_l

def part2(s):
    rules, b = parse_input(s)

    answer = 0

    for l in b:
        if not verify(rules, l):
            l = reorder(rules, l)
            assert(verify(rules, l))
            answer += l[len(l)//2]

    lib.aoc.give_answer(2024, 5, 2, answer)

INPUT = lib.aoc.get_input(2024, 5)
part1(INPUT)
part2(INPUT)
