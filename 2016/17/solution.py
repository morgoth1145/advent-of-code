import hashlib

import lib.aoc

def generate_all_paths(s, width, height):
    OPEN_DOOR = 'bcdef'

    states = [(1, 1, '')]

    while True:
        new_states = []

        for x, y, path in states:
            if x == width and y == height:
                yield path
                continue

            h = hashlib.md5((s + path).encode()).hexdigest()
            up, down, left, right = h[:4]

            if x > 1 and left in OPEN_DOOR:
                new_states.append((x-1, y, path+'L'))
            if x < width and right in OPEN_DOOR:
                new_states.append((x+1, y, path+'R'))
            if y > 1 and up in OPEN_DOOR:
                new_states.append((x, y-1, path+'U'))
            if y < height and down in OPEN_DOOR:
                new_states.append((x, y+1, path+'D'))

        states = new_states

        if len(states) == 0:
            return

def part1(s):
    answer = min(generate_all_paths(s, 4, 4), key=len)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = max(map(len, generate_all_paths(s, 4, 4)))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 17)
part1(INPUT)
part2(INPUT)
