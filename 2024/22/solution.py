import collections
import numpy

import lib.aoc

def generate_rngs(s, num_to_gen, output_mod=16777216):
    rngs = numpy.array(list(map(int, s.splitlines())),
                       dtype=numpy.uint32)

    out = numpy.zeros((len(rngs), num_to_gen), dtype=numpy.int64)

    for i in range(num_to_gen):
        rngs = (rngs ^ (rngs << 6)) & 0xffffff
        rngs = (rngs ^ (rngs >> 5)) & 0xffffff
        rngs = (rngs ^ (rngs << 11)) & 0xffffff

        out[:,i] = rngs % output_mod

    return out

def part1(s):
    answer = numpy.sum(generate_rngs(s, 2000)[:,-1])

    lib.aoc.give_answer(2024, 22, 1, answer)

def make_delta_to_price_map(prices, deltas):
    c = {}

    delta_sequences = zip(deltas, deltas[1:], deltas[2:], deltas[3:])
    sell_prices = prices[4:]

    for key, price in zip(delta_sequences, sell_prices):
        if key not in c:
            c[key] = price

    return c

def part2(s):
    seller_arr = generate_rngs(s, 2000, output_mod=10)
    delta_arr = seller_arr[:,1:] - seller_arr[:,:-1]

    c = collections.Counter()

    for i in range(seller_arr.shape[0]):
        c += make_delta_to_price_map(seller_arr[i],
                                     delta_arr[i])

    answer = max(c.values())

    lib.aoc.give_answer(2024, 22, 2, answer)

INPUT = lib.aoc.get_input(2024, 22)
part1(INPUT)
part2(INPUT)
