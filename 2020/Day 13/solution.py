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

def find_bus_cadence(a, b, start, offset):
    n = start
    while (n-offset) % a != 0:
        n += b
    m = n+b
    while (m-offset) % a != 0:
        m += b
    return n, m-n

def part2(s):
    _, busses = s.splitlines()
    busses = [int(b) if b != 'x' else None
              for b in busses.split(',')][::-1]
    offset = 0
    cadence = busses[0]
    answer = busses[0]
    for b in busses[1:]:
        offset += 1
        if b is None:
            continue
        answer, cadence = find_bus_cadence(b, cadence, answer, offset)
    answer -= offset
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 13)

part1(INPUT)
part2(INPUT)
