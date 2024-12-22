import numpy

import lib.aoc

def generate_rngs(s, num_to_gen, output_mod=16777216, output_dtype=numpy.int64):
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

    seller_arr = generate_rngs(s, NUM_TO_GENERATE, output_mod=10, output_dtype=numpy.int8)
    num_sellers = seller_arr.shape[0]

    # Instead of a tuple, represent each delta sequence a as a single int.
    # Essentially, treat it as a base 19 number!
    DELTA_KEY_BASE = 19
    DELTA_KEY_OFFSET = 9 # Shift by 9 to keep delta values positive
    NUM_DELTA_KEYS = DELTA_KEY_BASE**4

    handled = numpy.zeros((num_sellers, NUM_DELTA_KEYS), dtype=numpy.bool_)
    # Track sell values per-seller initially. Otherwise if two sellers
    # match the same delta string at the same time then they won't both
    # be counted in the totals!
    sell_values = numpy.zeros((num_sellers, NUM_DELTA_KEYS), numpy.int8)

    all_sellers_key = numpy.arange(num_sellers)
    delta_key = numpy.zeros(num_sellers, numpy.int32)

    last_prices = seller_arr[:,0]

    for i in range(NUM_TO_GENERATE):
        # Drop the most significant "digit", shift, and add the new delta
        prices = seller_arr[:,i+1]
        delta = prices - last_prices + DELTA_KEY_OFFSET
        last_prices = prices
        delta_key = (delta_key * DELTA_KEY_BASE) % NUM_DELTA_KEYS + delta

        if i >= 3:
            # Get the old handled flags and update them in the matrix
            was_handled = handled[all_sellers_key, delta_key]
            to_handle = 1 - was_handled
            handled[all_sellers_key, delta_key] = True

            # Zero out any prices for sellers that already have this
            # delta sequence handled.
            price = prices * to_handle

            sell_values[all_sellers_key, delta_key] += price

    totals = numpy.zeros(NUM_DELTA_KEYS, numpy.int64)

    for s in range(num_sellers):
        totals += sell_values[s]

    answer = totals.max()

    lib.aoc.give_answer(2024, 22, 2, answer)

INPUT = lib.aoc.get_input(2024, 22)
part1(INPUT)
part2(INPUT)
