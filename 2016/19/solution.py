import lib.aoc

class Link:
    def __init__(self, n):
        self.n = n
        self.left = None
        self.right = None

def solve_linked_list(s, first_target, advance_fn):
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

def part1_linked_list(s):
    def advance_fn(current, remaining):
        return current.left.left

    answer = solve_linked_list(s, 1, advance_fn)

    print(f'The answer to part one is {answer}')

def part2_linked_list(s):
    def advance_fn(current, remaining):
        current = current.left
        if remaining % 2 == 1:
            # There was a tie, skip one
            current = current.left
        return current

    answer = solve_linked_list(s, int(s) // 2, advance_fn)

    print(f'The answer to part two is {answer}')

def part1_closed(s):
    # Part 1 is actually the Josephus problem and follows a very simple pattern
    # https://en.wikipedia.org/wiki/Josephus_problem#Bitwise
    n = int(s)
    max_power_of_2 = 1 << (n.bit_length() - 1)
    answer = ((n - max_power_of_2) << 1) + 1

    print(f'The answer to part one is {answer}')

def part2_semi_closed(s):
    # Part 2 also follows a simple sequence. I'm not sure if it has a name, but
    # the solutions are as follows for 1 elf, 2 elves, 3 elves, etc.
    # 1, 1, 3, 1, 2, 3, 5, 7, 9, 1, 2, 3, ...
    # Essentially, count up sequentially to n then skip every other number until
    # m, then start over. n is the last m, and m is n*3, where n and m start
    # at 1 and 1
    # There may be a closed form solution, but this allows for a super-fast
    # calculation
    remaining = int(s)

    # Special case the first iteration
    if remaining > 1:
        remaining -= 1

    n = 1
    m = 3
    while remaining > 2*n:
        remaining -= 2*n
        n, m = m, m*3

    if remaining <= n:
        answer = remaining
    else:
        answer = ((remaining - n) << 1) + n

    print(f'The answer to part two is {answer}')

part1 = part1_closed
part2 = part2_semi_closed

INPUT = lib.aoc.get_input(2016, 19)
part1(INPUT)
part2(INPUT)
