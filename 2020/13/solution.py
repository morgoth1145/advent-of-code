import lib.aoc
import lib.math

def parse_notes(s):
    timestamp, rest = s.splitlines()
    rest = rest.split(',')
    busses = [int(b) for b in rest if b != 'x']
    offsets = [idx for idx,b in enumerate(rest) if b != 'x']
    return int(timestamp), busses, offsets

def part1(s):
    timestamp, busses, _ = parse_notes(s)
    available_times = []
    for b in busses:
        time_available = ((timestamp+b-1) // b) * b
        available_times.append((time_available, b))
    best_time, best_bus = min(available_times)
    answer = (best_time-timestamp) * best_bus
    lib.aoc.give_answer(2020, 13, 1, answer)

def part2(s):
    _, busses, offsets = parse_notes(s)
    answer = lib.math.offset_chinese_remainder(zip(busses, offsets))
    lib.aoc.give_answer(2020, 13, 2, answer)

INPUT = lib.aoc.get_input(2020, 13)

part1(INPUT)
part2(INPUT)
