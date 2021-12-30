import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        deer, _, _, speed, _, _, duration, _, _, _, _, _, _, rest, _ = line.split()
        speed = int(speed)
        duration = int(duration)
        rest = int(rest)
        yield deer, speed, duration, rest

def calc_distance(speed, duration, rest, total_time):
    full_cycle = duration + rest
    cycle_count, leftover = divmod(total_time, full_cycle)
    leftover = min(leftover, duration)

    move_time = cycle_count * duration + leftover
    return speed * move_time

def part1(s):
    answer = max(calc_distance(speed, duration, rest, 2503)
                 for deer, speed, duration, rest in parse_input(s))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 14)
part1(INPUT)
part2(INPUT)
