import math

import helpers.input

def parse_notes(s):
    timestamp, busses = s.splitlines()
    busses = [(int(b), idx)
              for idx, b in enumerate(busses.split(','))
              if b != 'x']
    return int(timestamp), busses

def part1(s):
    timestamp, busses = parse_notes(s)
    available_times = []
    for b, _ in busses:
        time_available = ((timestamp+b-1) // b) * b
        available_times.append((time_available, b))
    best_time, best_bus = min(available_times)
    answer = (best_time-timestamp) * best_bus
    print(f'The answer to part one is {answer}')

def part2(s):
    _, busses = parse_notes(s)
    time = 1
    cadence = 1
    for b, offset in busses:
        tries = 0
        while (time+offset) % b != 0:
            time += cadence
            tries += 1
            if tries == b:
                print('There is no answer!')
                return
        cadence *= b // math.gcd(cadence, b)
    answer = time
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 13)

part1(INPUT)
part2(INPUT)
