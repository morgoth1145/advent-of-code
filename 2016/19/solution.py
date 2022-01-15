import lib.aoc

class Link:
    def __init__(self, n):
        self.n = n
        self.left = None
        self.right = None

def part1(s):
    elves = list(map(Link, range(1, int(s)+1)))

    for left, right in zip(elves + [elves[0]], [elves[-1]] + elves):
        left.right = right
        right.left = left

    current = elves[0]
    while current.left != current:
        new_left = current.left.left
        current.left = new_left
        new_left.right = current
        current = new_left

    answer = current.n

    print(f'The answer to part one is {answer}')

def part2(s):
    elves = list(map(Link, range(1, int(s)+1)))

    for left, right in zip(elves + [elves[0]], [elves[-1]] + elves):
        left.right = right
        right.left = left

    # We don't care *who* steals, we care who is removed!
    remaining = len(elves)
    to_remove = remaining // 2

    current_target = elves[to_remove]

    while remaining > 1:
        left = current_target.left
        right = current_target.right
        left.right = right
        right.left = left

        # Update current target
        if remaining % 2 == 1:
            # There was a tie, skip one
            current_target = left.left
        else:
            current_target = left

        remaining -= 1

    answer = current_target.n

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 19)
part1(INPUT)
part2(INPUT)
