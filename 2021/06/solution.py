import lib.aoc

def iterate(fish_timers):
    new_timers = [t-1 for t in fish_timers]
    for idx, t in enumerate(fish_timers):
        if t == 0:
            # This fish reproduced!
            new_timers[idx] = 6
            new_timers.append(8)
    return new_timers

def part1(s):
    fish_timers = list(map(int, s.split(',')))

    for _ in range(80):
        fish_timers = iterate(fish_timers)

    answer = len(fish_timers)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 6)
part1(INPUT)
part2(INPUT)
