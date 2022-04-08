import lib.aoc

def part1(s):
    groups = s.split('\n\n')
    answer = 0
    for g in groups:
        g = ''.join(g.split())
        answer += len(set(g))
    lib.aoc.give_answer(2020, 6, 1, answer)

def part2(s):
    groups = s.split('\n\n')
    answer = 0
    for g in groups:
        people = g.split()
        all_yes = set(people[0])
        for p in people[1:]:
            all_yes &= set(p)
        answer += len(set(all_yes))
    lib.aoc.give_answer(2020, 6, 2, answer)

INPUT = lib.aoc.get_input(2020, 6)
part1(INPUT)
part2(INPUT)
