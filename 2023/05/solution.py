import lib.aoc

def solve(s, seed_interpreter):
    groups = s.split('\n\n')

    seed_ranges = seed_interpreter(list(map(int, groups[0].split()[1:])))

    for g in groups[1:]:
        step_mapping = [tuple(map(int, l.split()))
                        for l in g.splitlines()[1:]]

        new_ranges = []

        for start, r_len in seed_ranges:
            while r_len != 0:
                found_match = False
                best_dist = r_len

                for dst, src, length in step_mapping:
                    if src <= start < src+length:
                        # Found a match
                        off = start - src
                        rem_length = min(length - off, r_len)
                        new_ranges.append((dst+off, rem_length))
                        start += rem_length
                        r_len -= rem_length
                        found_match = True
                        break
                    else:
                        if start < src:
                            best_dist = min(src - start, best_dist)

                if not found_match:
                    handling_len = min(best_dist, r_len)
                    new_ranges.append((start, handling_len))
                    start += handling_len
                    r_len -= handling_len

        seed_ranges = new_ranges

    return min(start for start, length in seed_ranges)

def part1(s):
    def seed_interpreter(nums):
        return [(n, 1) for n in nums]

    answer = solve(s, seed_interpreter)

    lib.aoc.give_answer(2023, 5, 1, answer)

def part2(s):
    def seed_interpreter(nums):
        return list(zip(nums[::2], nums[1::2]))

    answer = solve(s, seed_interpreter)

    lib.aoc.give_answer(2023, 5, 2, answer)

INPUT = lib.aoc.get_input(2023, 5)
part1(INPUT)
part2(INPUT)
