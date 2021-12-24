import lib.aoc

def solve_not_really_mostly_analyzed_by_hand_ouch(s, optimize_fn):
    lines = s.splitlines()
    assert(len(lines) == 18 * 14)

    FUNC_PROTO = '''inp w
mul x 0
add x z
mod x 26
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
mul y x
add z y'''

    stack = []
    digits = [0] * 14

    # The iteations boil down to this. After stupid amounts of analysis. Ouch
    # if z % 26 + {B} != w:
    #     z //= {A} # Either 26 or 1
    #     z = 26 * z + w + {C}
    # else:
    #     z //= {A} # Either 26 or 1
    for group_idx, idx in enumerate(range(0, len(lines), 18)):
        group = lines[idx:idx+18]
        C = int(group.pop(15).split()[2])
        B = int(group.pop(5).split()[2])
        A = int(group.pop(4).split()[2])

        assert('\n'.join(group) == FUNC_PROTO)

        if B >= 10:
            assert(A == 1)
            # Forced condition failure, z is never negative
            stack.append((group_idx, C))
        else:
            assert(A == 26)
            prev_idx, prev_C = stack.pop(-1)
            offset = prev_C + B
            prev_d = optimize_fn(d for d in range(1, 10)
                                 if d + offset in range(1, 10))
            cur_d = prev_d + offset
            digits[prev_idx] = prev_d
            digits[group_idx] = cur_d

    assert(len(stack) == 0)

    return int(''.join(map(str, digits)))

def part1(s):
    answer = solve_not_really_mostly_analyzed_by_hand_ouch(s, max)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve_not_really_mostly_analyzed_by_hand_ouch(s, min)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 24)
part1(INPUT)
part2(INPUT)
