import lib.aoc

def concat_nums(a, b):
    mult = 1
    while mult <= b:
        mult *= 10
    return a*mult+b

def solve(s, allow_concatenation=False):
    def is_fixable_equation(target, current_val, parts):
        if current_val > target:
            # All operations grow the number, if we've passed the target
            # it is not fixable!
            return False

        if len(parts) == 0:
            return current_val == target

        a = parts[0]
        parts = parts[1:]

        return (is_fixable_equation(target, current_val+a, parts) or
                is_fixable_equation(target, current_val*a, parts) or
                (allow_concatenation and
                 is_fixable_equation(target, concat_nums(current_val, a), parts)))

    answer = 0

    for line in s.splitlines():
        target, parts = line.split(':')

        target = int(target)
        parts = tuple(map(int, parts.split()))

        if is_fixable_equation(target, parts[0], parts[1:]):
            answer += target

    return answer

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2024, 7, 1, answer)

def part2(s):
    answer = solve(s, allow_concatenation=True)

    lib.aoc.give_answer(2024, 7, 2, answer)

INPUT = lib.aoc.get_input(2024, 7)
part1(INPUT)
part2(INPUT)
