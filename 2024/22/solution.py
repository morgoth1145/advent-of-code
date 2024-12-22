import lib.aoc

def generate_random(seed):
    secret = seed
    while True:
        res = secret * 64
        secret = res ^ secret
        secret = secret % 16777216
        res = secret // 32
        secret = res ^ secret
        secret = secret % 16777216
        res = secret * 2048
        secret = res ^ secret
        secret = secret % 16777216
        yield secret

def get_nth_num(seq, n):
    for _ in range(n):
        val = next(seq)

    return val

def part1(s):
    nums = list(map(int, s.splitlines()))

    answer = sum(get_nth_num(generate_random(seed), 2000)
                 for seed in nums)

    lib.aoc.give_answer(2024, 22, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 22)
part1(INPUT)
part2(INPUT)
