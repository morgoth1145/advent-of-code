import helpers.input

def part1(s):
    timestamp, rest = s.splitlines()
    timestamp = int(timestamp)
    rest = rest.split(',')
    best = None
    for n in rest:
        if n == 'x':
            continue
        n = int(n)
        time = (timestamp // n) * n
        while time < timestamp:
            time += n
        if best is None:
            best = (time, n)
        elif best[0] > time:
            best = (time, n)
    answer = (best[0] - timestamp) * best[1]
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 13)

part1(INPUT)
part2(INPUT)
