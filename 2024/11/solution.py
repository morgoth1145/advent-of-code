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

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 11)
part1(INPUT)
part2(INPUT)
