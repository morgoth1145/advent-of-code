import lib.aoc
import lib.symbolic_math

def solve_via_decompiled_analysis(s, optimize_fn):
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

def run_alu(s, variable_options, target_var, target_val):
    def impl(instructions, state, inputs):
        for idx, inst in enumerate(instructions):
            parts = inst.split()
            op = parts[0]
            dest = parts[1]
            leftval = state[dest]
            if 3 == len(parts):
                right = parts[2]
                if right in 'wxyz':
                    rightval = state[right]
                else:
                    rightval = int(right)

            if op == 'eql':
                new_expr = leftval - rightval

                zero_solutions = []
                nonzero_solutions = []

                for result, substitution in new_expr.gen_substitutions():
                    if result == 0:
                        zero_solutions.append(substitution)
                    else:
                        nonzero_solutions.append(substitution)

                assert(len(zero_solutions) + len(nonzero_solutions) > 0)

                def reduce_solutions(solutions):
                    if 0 == len(solutions):
                        return []

                    symbols = [s for s,v in solutions[0]]
                    symbol_cands = [set() for s in symbols]

                    for substitutions in solutions:
                        for idx, (s, v) in enumerate(substitutions):
                            assert(symbols[idx] == s)
                            symbol_cands[idx].add(v)

                    def gen_all_options(idx, test_idx, test_s):
                        if idx == len(symbols):
                            yield tuple()
                            return

                        s = symbols[idx]
                        if idx == test_idx:
                            cands = test_s.options
                        else:
                            cands = symbol_cands[idx]

                        for o in cands:
                            for sub_opt in gen_all_options(idx+1,
                                                           test_idx,
                                                           test_s):
                                yield ((s, o),) + sub_opt

                    sol_set = set(solutions)
                    unneeded_symbols = set()

                    for idx, test_s in enumerate(symbols):
                        if symbol_cands[idx] != set(test_s.options):
                            # Not even fully represented! Don't bother trying!
                            continue
                        if all(opt in sol_set
                               for opt in gen_all_options(0, idx, test_s)):
                            unneeded_symbols.add(test_s)

                    new_solutions = []
                    seen = set()
                    for substitution in solutions:
                        new_sub = tuple((s, v)
                                        for s, v in substitution
                                        if s not in unneeded_symbols)
                        if new_sub in seen:
                            continue
                        seen.add(new_sub)
                        new_solutions.append(new_sub)

                    return new_solutions

                nonzero_solutions = reduce_solutions(nonzero_solutions)
                zero_solutions = reduce_solutions(zero_solutions)

                if len(zero_solutions):
                    # This can be equal! Try result as 1
                    new_state = dict(state.items())
                    new_state[dest] = lib.symbolic_math.Expression([(1, tuple())])
                    for sub_sol in impl(instructions[idx+1:],
                                        new_state,
                                        inputs):
                        for sol in zero_solutions:
                            yield sol + sub_sol

                if len(nonzero_solutions):
                    # This can be unequal! Try result as 0
                    new_state = dict(state.items())
                    new_state[dest] = lib.symbolic_math.Expression([(0, tuple())])
                    for sub_sol in impl(instructions[idx+1:],
                                        new_state,
                                        inputs):
                        for sol in nonzero_solutions:
                            yield sol + sub_sol

                return

            if op == 'inp':
                name = f'input{len(inputs)}'
                outval = lib.symbolic_math.Symbol(name, variable_options)
                inputs.append(outval)
            elif op == 'add':
                outval = leftval + rightval
            elif op == 'mul':
                outval = leftval * rightval
            elif op == 'div':
                outval = leftval // rightval
            elif op == 'mod':
                outval = leftval % rightval
            else:
                print('Unknown instruction!')
                assert(False)

            state[dest] = outval

        e = state[target_var]
        for result, substitutions in e.gen_substitutions():
            if result == target_val:
                yield substitutions

    state = {
        v:lib.symbolic_math.Expression()
        for v in 'wxyz'
    }
    yield from impl(s.splitlines(), state, [])

def solve_programmatically(s, optimize_fn):
    best = None

    for substitutions in run_alu(s, range(1, 10), 'z', 0):
        digits = [0] * 14
        for s, d in substitutions:
            idx = int(s.name[5:])
            digits[idx] = d
        num = int(''.join(map(str, digits)))

        if best is None or optimize_fn(best, num) != best:
            best = num

    return best

##solve = solve_via_decompiled_analysis
solve = solve_programmatically

def part1(s):
    answer = solve(s, max)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, min)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 24)
part1(INPUT)
part2(INPUT)
