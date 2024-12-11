import functools

import lib.aoc

def blink(stones):
    n = []
    for i, s in enumerate(stones):
        if s == 0:
            n.append(1)
            continue
        digits = str(s)
        if len(digits) % 2 == 0:
            left = digits[:len(digits)//2]
            right = digits[len(digits)//2:]
            n.append(int(left))
            n.append(int(right))
            continue
        n.append(s*2024)
    return n

def part1(s):
    stones = tuple(map(int, s.split()))

    for _ in range(25):
        stones = blink(stones)

    answer = len(stones)

    lib.aoc.give_answer(2024, 11, 1, answer)

@functools.cache
def count_blink_stones(s, blinks_left):
    if blinks_left == 0:
        return 1

    if s == 0:
        return count_blink_stones(1, blinks_left-1)

    digits = str(s)
    if len(digits) % 2 == 0:
        left = digits[:len(digits)//2]
        right = digits[len(digits)//2:]
        left = count_blink_stones(int(left), blinks_left-1)
        right = count_blink_stones(int(right), blinks_left-1)
        return left + right

    return count_blink_stones(s*2024, blinks_left-1)

def part2(s):
    stones = tuple(map(int, s.split()))

    answer = sum(count_blink_stones(s, 75)
                 for s in stones)

    lib.aoc.give_answer(2024, 11, 2, answer)

INPUT = lib.aoc.get_input(2024, 11)
part1(INPUT)
part2(INPUT)
