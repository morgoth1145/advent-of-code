import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        parts = line.split()
        if parts[0] == 'turn':
            parts = parts[1:]
        op, start, _, end = parts
        x0,y0 = start.split(',')
        x1,y1 = end.split(',')
        yield op, (int(x0), int(y0)), (int(x1), int(y1))

def part1(s):
    states = {}
    for x in range(1000):
        for y in range(1000):
            states[x,y] = False

    for op, (x0, y0), (x1, y1) in parse_input(s):
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                if op == 'on':
                    states[x,y] = True
                elif op == 'off':
                    states[x,y] = False
                else:
                    states[x,y] = not states[x,y]

    answer = sum(states.values())

    print(f'The answer to part one is {answer}')

def part2(s):
    states = {}
    for x in range(1000):
        for y in range(1000):
            states[x,y] = 0

    for op, (x0, y0), (x1, y1) in parse_input(s):
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                if op == 'on':
                    states[x,y] += 1
                elif op == 'off':
                    states[x,y] = max(states[x,y]-1, 0)
                else:
                    states[x,y] += 2

    answer = sum(states.values())

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 6)
part1(INPUT)
part2(INPUT)
