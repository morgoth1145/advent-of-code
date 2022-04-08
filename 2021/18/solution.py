import json

import lib.aoc

def explode_num(num):
    def add_to_rightmost(num, val):
        if isinstance(num, int):
            return num + val
        a, b = num
        return [a, add_to_rightmost(b, val)]

    # Returns left_val, new_num, right_val
    def impl(num, depth, right_val):
        if isinstance(num, int):
            return 0, num+right_val, 0

        a, b = num
        if depth == 4:
            return a+right_val, 0, b

        left_val, a, right_val = impl(a, depth+1, right_val)
        left_val_b, b, right_val = impl(b, depth+1, right_val)
        if left_val_b > 0:
            a = add_to_rightmost(a, left_val_b)

        return left_val, [a, b], right_val

    _, new_num, _ = impl(num, 0, 0)
    return new_num

def split_num(num):
    if isinstance(num, int):
        if num > 9:
            d, m = divmod(num, 2)
            return [d, d + m]
        return None

    a, b = num

    new_a = split_num(a)
    if new_a is not None:
        return [new_a, b]

    new_b = split_num(b)
    if new_b is not None:
        return [a, new_b]

    return None

def reduce_num(num):
    while True:
        num = explode_num(num)
        new_num = split_num(num)
        if new_num is None:
            return num

        num = new_num

def magnitude(num):
    if isinstance(num, int):
        return num

    a, b = num
    return 3*magnitude(a) + 2*magnitude(b)

def part1(s):
    nums = list(map(reduce_num, map(json.loads, s.splitlines())))

    n = nums[0]
    for item in nums[1:]:
        n = reduce_num([n, item])

    answer = magnitude(n)

    lib.aoc.give_answer(2021, 18, 1, answer)

def part2(s):
    nums = list(map(reduce_num, map(json.loads, s.splitlines())))

    answer = max(magnitude(reduce_num([a, b]))
                 for ia, a in enumerate(nums)
                 for ib, b in enumerate(nums)
                 if ia != ib)

    lib.aoc.give_answer(2021, 18, 2, answer)

INPUT = lib.aoc.get_input(2021, 18)
part1(INPUT)
part2(INPUT)
