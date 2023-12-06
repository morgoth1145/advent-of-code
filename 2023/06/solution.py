import lib.aoc

def solve(s):
    times, distances = s.splitlines()
    times = map(int, times.split(':')[1].split())
    distances = map(int, distances.split(':')[1].split())

    answer = 1

    for time, dist in zip(times, distances):
        # Binary search to find the minimum time which wins
        low, high = 1, (time+1) // 2
        while high - low > 1:
            mid = (low + high) // 2
            if mid * (time - mid) > dist:
                high = mid
            else:
                low = mid

        # high is the lowest time which wins the race
        t = high
        remaining = time - t
        # All times between t and remaining (inclusive) will win
        # As such we just need to count how many times that is to know
        # how many winning options there are
        answer *= (remaining - t + 1)

    return answer

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2023, 6, 1, answer)

def part2(s):
    answer = solve(s.replace(' ', ''))

    lib.aoc.give_answer(2023, 6, 2, answer)

INPUT = lib.aoc.get_input(2023, 6)
part1(INPUT)
part2(INPUT)
