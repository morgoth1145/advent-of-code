import lib.aoc

def part1(s):
    lines = s.splitlines()

    answer = 0

    for sack in lines:
        a = sack[:len(sack)//2]
        b = sack[len(sack)//2:]
        shared = set(a) & set(b)
        assert(len(shared) == 1)

        shared = list(shared)[0]

        answer += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(shared) + 1

    lib.aoc.give_answer(2022, 3, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 3)
part1(INPUT)
part2(INPUT)
