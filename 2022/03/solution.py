import lib.aoc

def score_shared_item(*groups):
    shared = set(groups[0])
    for s in groups[1:]:
        shared &= set(s)

    shared = list(shared)[0]
    if shared.islower():
        return ord(shared) - ord('a') + 1
    else:
        assert(shared.isupper())
        return ord(shared) - ord('A') + 27

def part1(s):
    answer = sum(score_shared_item(sack[:len(sack)//2],
                                   sack[len(sack)//2:])
                 for sack in s.splitlines())

    lib.aoc.give_answer(2022, 3, 1, answer)

def part2(s):
    sacks = s.splitlines()

    answer = sum(score_shared_item(a, b, c)
                 for (a, b, c) in (sacks[i:i+3]
                                   for i in range(0, len(sacks), 3)))

    lib.aoc.give_answer(2022, 3, 2, answer)

INPUT = lib.aoc.get_input(2022, 3)
part1(INPUT)
part2(INPUT)
