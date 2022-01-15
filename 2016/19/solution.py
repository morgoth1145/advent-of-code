import lib.aoc

class Link:
    def __init__(self, n):
        self.n = n
        self.left = None
        self.right = None

def solve(s, first_target, advance_fn):
    elves = list(map(Link, range(1, int(s)+1)))

    for left, right in zip(elves + [elves[0]], [elves[-1]] + elves):
        left.right = right
        right.left = left

    remaining = len(elves)
    current = elves[first_target]

    while remaining > 1:
        current.left.right = current.right
        current.right.left = current.left
        current = advance_fn(current, remaining)
        remaining -= 1

    return current.n

def part1(s):
    def advance_fn(current, remaining):
        return current.left.left

    answer = solve(s, 1, advance_fn)

    print(f'The answer to part one is {answer}')

def part2(s):
    def advance_fn(current, remaining):
        current = current.left
        if remaining % 2 == 1:
            # There was a tie, skip one
            current = current.left
        return current

    answer = solve(s, int(s) // 2, advance_fn)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 19)
part1(INPUT)
part2(INPUT)
