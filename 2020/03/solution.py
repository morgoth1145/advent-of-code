import lib.aoc

def count_tree_hits(s, right, down):
    answer = 0
    x = 0
    for line in s.splitlines()[::down]:
        if line[x % len(line)] == '#':
            answer += 1
        x += right
    return answer

def part1(s):
    answer = count_tree_hits(s, 3, 1)
    lib.aoc.give_answer(2020, 3, 1, answer)

def part2(s):
    answer = 1
    for right, down in ((1,1),
                        (3,1),
                        (5,1),
                        (7,1),
                        (1,2)):
        answer *= count_tree_hits(s, right, down)
    lib.aoc.give_answer(2020, 3, 2, answer)

INPUT = lib.aoc.get_input(2020, 3)
part1(INPUT)
part2(INPUT)
