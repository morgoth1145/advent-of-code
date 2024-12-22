import collections

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

def get_seller_prices(seed):
    generator = generate_random(seed)
    prices = []
    while len(prices) < 2000:
        prices.append(next(generator) % 10)
    return prices

def make_sell_map(prices):
    c = collections.Counter()

    deltas = [b-a for a,b in zip(prices, prices[1:])]

    for i in range(len(prices)):
        if i+4 >= len(deltas):
            break
        key = tuple(deltas[i+dd] for dd in range(4))
        if key in c:
            continue
        c[key] = prices[i+4]

    return c

def part2(s):
    nums = list(map(int, s.splitlines()))

    sellers = list(map(get_seller_prices, nums))

    c = collections.Counter()

    for prices in sellers:
        c += make_sell_map(prices)

    answer = max(c.values())

    lib.aoc.give_answer(2024, 22, 2, answer)

INPUT = lib.aoc.get_input(2024, 22)
part1(INPUT)
part2(INPUT)
