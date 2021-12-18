import lib.aoc

def explode_num(num):
    def add_to_leftmost(num, val):
        if isinstance(num, int):
            return num + val
        a, b = num
        return [add_to_leftmost(a, val), b]

    def add_to_rightmost(num, val):
        if isinstance(num, int):
            return num + val
        a, b = num
        return [a, add_to_rightmost(b, val)]

    # Returns exploded, left_exp, new_num, right_exp
    def impl(num, depth):
        if isinstance(num, int):
            return False, None, num, None

        a, b = num
        if depth == 4:
            return True, a, 0, b

        exploded, left_exp, a, right_exp = impl(a, depth+1)
        if exploded:
            if right_exp is not None:
                b = add_to_leftmost(b, right_exp)
                right_exp = None
        else:
            exploded, left_exp, b, right_exp = impl(b, depth+1)

            if left_exp is not None:
                a = add_to_rightmost(a, left_exp)
                left_exp = None

        return exploded, left_exp, [a, b], right_exp

    exploded, _, new_num, _ = impl(num, 0)
    return new_num if exploded else None

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
        new_num = explode_num(num)
        if new_num is not None:
            num = new_num
            continue

        new_num = split_num(num)
        if new_num is not None:
            num = new_num
            continue

        return num

def magnitude(num):
    if isinstance(num, int):
        return num

    a, b = num
    return 3*magnitude(a) + 2*magnitude(b)

def part1(s):
    nums = list(map(reduce_num, map(eval, s.splitlines())))

    n = nums[0]
    for item in nums[1:]:
        n = reduce_num([n, item])

    answer = magnitude(n)

    print(f'The answer to part one is {answer}')

def part2(s):
    nums = list(map(reduce_num, map(eval, s.splitlines())))

    answer = max(magnitude(reduce_num([a, b]))
                 for ia, a in enumerate(nums)
                 for ib, b in enumerate(nums)
                 if ia != ib)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 18)
part1(INPUT)
part2(INPUT)
