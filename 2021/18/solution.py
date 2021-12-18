import lib.aoc

def add(a, b):
    return [a, b]

DIGITS = '0123456789'

def try_explode(num):
    num_str = str(num).replace(' ', '')
    depth = 0
    for idx, c in enumerate(num_str):
        if c == '[':
            depth += 1
            if depth == 5:
                # Explode!
                end_idx = num_str.find(']', idx)
                a, b = list(map(int, num_str[idx+1:end_idx].split(',')))
                left = num_str[:idx]
                for lidx in range(len(left)-1, -1, -1):
                    c = left[lidx]
                    if c in DIGITS:
                        term = max(i for i in range(lidx)
                                   if left[i] not in DIGITS)
                        val = int(left[term+1:lidx+1])
                        val += a
                        left = left[:term+1] + str(val) + left[lidx+1:]
                        break
                mid = '0'
                right = num_str[end_idx+1:]
                for ridx, c in enumerate(right):
                    if c in DIGITS:
                        term = min(i for i in range(ridx+1, len(right))
                                   if right[i] not in DIGITS)
                        val = int(right[ridx:term])
                        val += b
                        right = right[:ridx] + str(val) + right[term:]
                        break
                return eval(left + mid + right)
        elif c == ']':
            depth -= 1
    return None

def try_split(num):
    if isinstance(num, list):
        a, b = num
        new_a = try_split(a)
        if new_a is not None:
            return [new_a, b]
        new_b = try_split(b)
        if new_b is not None:
            return [a, new_b]
        return None
    if num > 9:
        d, m = divmod(num, 2)
        return [d, d + m]
    return None

def reduce(num):
    while True:
        new_num = try_explode(num)
        if new_num is not None:
            num = new_num
            continue
        new_num = try_split(num)
        if new_num is not None:
            num = new_num
            continue
        return num

def magnitude(num):
    if isinstance(num, list):
        a, b = num
        a = magnitude(a)
        b = magnitude(b)
        return 3*a + 2*b
    return num

def part1(s):
    lines = s.splitlines()
    fake_nums = list(map(eval, lines))

    num = fake_nums[0]

    for item in fake_nums[1:]:
        item = reduce(item)
        num = reduce(add(num, item))

    answer = magnitude(num)

    print(f'The answer to part one is {answer}')

def part2(s):
    lines = s.splitlines()
    fake_nums = list(map(eval, lines))

    fake_nums = list(map(reduce, fake_nums))

    best = 0
    for ia, a in enumerate(fake_nums):
        for ib, b in enumerate(fake_nums):
            if ia == ib:
                continue

            mag = magnitude(reduce(add(a, b)))
            best = max(best, mag)

    answer = best

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 18)
part1(INPUT)
part2(INPUT)
