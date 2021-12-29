import lib.aoc
import lib.symbolic_math

def run_alu(s, inputs, target_var, target_val):
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
                equality = lib.symbolic_math.Equality(leftval, rightval)
                inequality = lib.symbolic_math.Inequality(leftval, rightval)

                for res, constraint in [(1, equality),
                                        (0, inequality)]:
                    if constraint.satisfiable:
                        new_state = dict(state.items())
                        new_state[dest] = lib.symbolic_math.Constant(res)
                        for sub_constraints in impl(instructions[idx+1:],
                                                    new_state,
                                                    inputs):
                            yield [constraint] + sub_constraints

                return

            if op == 'inp':
                outval, inputs = inputs[0], inputs[1:]
            elif op == 'add':
                outval = leftval + rightval
            elif op == 'mul':
                outval = leftval * rightval
            elif op == 'div':
                outval = leftval // rightval
            elif op == 'mod':
                outval = leftval % rightval
            else:
                print(f'Unknown instruction {inst}!')
                assert(False)

            state[dest] = outval

        equality = lib.symbolic_math.Equality(state[target_var], target_val)

        if equality.satisfiable:
            yield [equality]

    state = {
        v:lib.symbolic_math.Constant(0)
        for v in 'wxyz'
    }
    yield from impl(s.splitlines(), state, inputs)

def find_solution(constraints, inputs, digit_search_order):
    if 0 == len(inputs):
        return ''

    s, rest = inputs[0], inputs[1:]

    for d in digit_search_order:
        new_constraints = [c.substitute(s, d)
                           for c in constraints]
        new_constraints = [c for c in new_constraints
                           if not c.forced]
        if all(c.satisfiable for c in new_constraints):
            solution = find_solution(new_constraints, rest, digit_search_order)
            if solution is not None:
                return str(d) + solution

def solve(s, digit_search_order, optimize_fn):
    input_domain = lib.symbolic_math.IntegerDomain(1, 9)
    inputs = [lib.symbolic_math.Symbol(f'input{n}', input_domain)
              for n in range(s.count('inp'))]

    return int(optimize_fn(find_solution(constraints, inputs, digit_search_order)
                           for constraints in run_alu(s, inputs, 'z', 0)))

def part1(s):
    answer = solve(s, range(9, 0, -1), max)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, range(1, 10), min)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 24)
part1(INPUT)
part2(INPUT)
