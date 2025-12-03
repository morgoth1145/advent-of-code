import lib.aoc

def solve(s, num_batteries):
    def get_max(nums, to_choose):
        if to_choose == 0:
            return 0

        assert(len(nums) >= to_choose)

        best = -1
        best_i = None
        for i in range(len(nums) - to_choose + 1):
            v = nums[i]
            if v > best:
                best = v
                best_i = i

        return best * 10 ** (to_choose - 1) + get_max(nums[best_i+1:],
                                                      to_choose-1)

    answer = 0

    for row in s.splitlines():
        answer += get_max(tuple(map(int, row)), num_batteries)

    return answer

def part1(s):
    answer = solve(s, 2)

    lib.aoc.give_answer(2025, 3, 1, answer)

def part2(s):
    answer = solve(s, 12)

    lib.aoc.give_answer(2025, 3, 2, answer)

INPUT = lib.aoc.get_input(2025, 3)
part1(INPUT)
part2(INPUT)
