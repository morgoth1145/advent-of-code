import lib.aoc

def run_race(s, total_time):
    deer = []
    for line in s.splitlines():
        _, _, _, speed, _, _, duration, _, _, _, _, _, _, rest, _ = line.split()
        speed = int(speed)
        duration = int(duration)
        rest = int(rest)
        deer.append((speed, duration, rest))

    dists = [0] * len(deer)
    scores = [0] * len(deer)
    cycle_time = [0] * len(deer)

    for _ in range(total_time):
        best = None
        best_i = []
        for i, (speed, duration, rest) in enumerate(deer):
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

    return dists, scores

def part1(s):
    answer = max(run_race(s, 2503)[0])

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = max(run_race(s, 2503)[1])

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 14)
part1(INPUT)
part2(INPUT)
