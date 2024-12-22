import numpy

import lib.aoc

def generate_rngs(s, num_to_gen, output_mod=16777216):
    rngs = numpy.array(list(map(int, s.splitlines())),
                       dtype=numpy.uint32)

    out = numpy.zeros((len(rngs), num_to_gen+1), dtype=numpy.int64)
    out[:,0] = rngs % output_mod

    for i in range(num_to_gen):
        rngs = (rngs ^ (rngs << 6)) & 0xffffff
        rngs = (rngs ^ (rngs >> 5)) & 0xffffff
        rngs = (rngs ^ (rngs << 11)) & 0xffffff

        out[:,i+1] = rngs % output_mod

    return out

def part1(s):
    answer = generate_rngs(s, 2000)[:,-1].sum()

    lib.aoc.give_answer(2024, 22, 1, answer)

def part2(s):
    NUM_TO_GENERATE = 2000

    seller_arr = generate_rngs(s, NUM_TO_GENERATE, output_mod=10)
    delta_arr = seller_arr[:,1:] - seller_arr[:,:-1]

    num_sellers = seller_arr.shape[0]

    handled = numpy.zeros((num_sellers,) + (19,)*4, dtype=numpy.bool_)
    # Track sell values per-seller initially. Otherwise if two sellers
    # match the same delta string at the same time then they won't both
    # be counted in the totals!
    sell_values = numpy.zeros((num_sellers,) + (19,)*4, numpy.int64)

    all_sellers_key = numpy.arange(num_sellers)

    for i in range(NUM_TO_GENERATE-3):
        d0 = delta_arr[:,i]
        d1 = delta_arr[:,i+1]
        d2 = delta_arr[:,i+2]
        d3 = delta_arr[:,i+3]

        # Get the old handled flags and update them in the matrix
        was_handled = handled[all_sellers_key, d0, d1, d2, d3]
        to_handle = 1 - was_handled
        handled[all_sellers_key, d0, d1, d2, d3] = True

        # Extract the prices. Zero out any for sellers that already have this
        # delta sequence handled.
        price = seller_arr[:,i+4] * to_handle

        sell_values[all_sellers_key, d0, d1, d2, d3] += price

    totals = numpy.zeros((19,)*4, numpy.int64)

    for s in range(num_sellers):
        totals += sell_values[s]

    answer = totals.max()

    lib.aoc.give_answer(2024, 22, 2, answer)

INPUT = lib.aoc.get_input(2024, 22)
part1(INPUT)
part2(INPUT)
