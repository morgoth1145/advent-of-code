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

def run_scored_race(all_deer, total_time):
    dists = [0] * len(all_deer)
    scores = [0] * len(all_deer)
    cycle_time = [0] * len(all_deer)

    for _ in range(total_time):
        best = None
        best_i = []
        for i, (name, speed, duration, rest) in enumerate(all_deer):
            if cycle_time[i] < duration:
                dists[i] += speed
            cycle_time[i] = (cycle_time[i] + 1) % (duration + rest)

            if best is None or best < dists[i]:
                best = dists[i]
                best_i = [i]
            elif best == dists[i]:
                best_i.append(i)

        for i in best_i:
            scores[i] += 1

    return scores

def part2(s):
    answer = max(run_scored_race(list(parse_input(s)), 2503))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 14)
part1(INPUT)
part2(INPUT)
