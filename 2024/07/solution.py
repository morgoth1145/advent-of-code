import lib.aoc

def solve(s, allow_concatenation=False):
    # All numbers must be positive for this to work
    assert('-' not in s)

    def is_fixable_equation(target, parts):
        parts = list(parts)
        potential_targets = {target}

        while len(parts):
            n = parts.pop()

            new_potential_targets = set()

            for t in potential_targets:
                # Addition, only valid if the previous value is nonzero
                prev = t - n
                if prev >= 0:
                    new_potential_targets.add(prev)

                # Multiplication, only valid if t/n is whole and nonzero
                if t >= n and t % n == 0:
                    new_potential_targets.add(t // n)

                # Concatenation, only valid if the last digits match
                if allow_concatenation:
                    n2 = n
                    good = True
                    while n2 > 0:
                        if n2 % 10 == t % 10:
                            t //= 10
                            n2 //= 10
                        else:
                            good = False
                            break
                    if good:
                        new_potential_targets.add(t)

            potential_targets = new_potential_targets

        return 0 in potential_targets

    answer = 0

    for line in s.splitlines():
        target, parts = line.split(':')

        target = int(target)
        parts = tuple(map(int, parts.split()))

        if is_fixable_equation(target, parts):
            answer += target
            continue

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
