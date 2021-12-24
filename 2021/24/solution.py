import lib.aoc

def part1(s):
    lines = s.splitlines()
    assert(len(lines) == 18 * 14)

    FUNC_TEMPLATE = '''inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y'''.splitlines()
    SPECIAL = (4, 5, 15)

    iterations = []
    for idx in range(0, len(lines), 18):
        iterations.append(lines[idx:idx+18])

    iter_vars = []

    # Verify that the function template matches
    for idx, func in enumerate(iterations):
        variables = [0] * 3
        for j, line in enumerate(func):
            if j in SPECIAL:
                _, _, val = line.split()
                variables[SPECIAL.index(j)] = int(val)
                continue
            assert(line == FUNC_TEMPLATE[j])
        iter_vars.append(tuple(variables))

    # Function
    # A is either 26 or 1
    # B varies and is sometimes negative
    # C is *never* negative!
    '''
    if last_z % 26 + {B} != w:
        z //= {A} # Either 26 or 1
        z = 26 * z + w + {C}
    else:
        z //= {A} # Either 26 or 1
    '''

    CAND_DIGITS = range(1, 10)

    digits = [0] * 14

    stack = []
    for idx, (A, B, C) in enumerate(iter_vars):
        if B >= 10:
            assert(A == 1)
            # Forced fail, z is never negative
            stack.append((idx, C))
        else:
            # We need to *not* fail!
            assert(A == 26)
            prev_idx, prev_C = stack.pop(-1)
            combined = prev_C + B
            prev_d = max(d for d in CAND_DIGITS
                         if d + combined in CAND_DIGITS)
            cur_d = prev_d + combined
            digits[prev_idx] = prev_d
            digits[idx] = cur_d

    answer = int(''.join(map(str, digits)))

    assert(len(stack) == 0)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 24)
part1(INPUT)
part2(INPUT)
