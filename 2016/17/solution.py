import hashlib

import lib.aoc

OPEN_DOOR = 'bcdef'

def determine_doors(s, path):
    h = hashlib.md5((s + path).encode()).hexdigest()
    up, down, left, right = h[:4]
    up = up in OPEN_DOOR
    down = down in OPEN_DOOR
    left = left in OPEN_DOOR
    right = right in OPEN_DOOR
    return up, down, left, right

def shortest_path(s, width, height):
    states = [(1, 1, '')]

    while True:
        new_states = []

        for x, y, path in states:
            if x == width and y == height:
                return path

            up, down, left, right = determine_doors(s, path)
            if x > 1 and left:
                new_states.append((x-1, y, path+'L'))
            if x < width and right:
                new_states.append((x+1, y, path+'R'))
            if y > 1 and up:
                new_states.append((x, y-1, path+'U'))
            if y < height and down:
                new_states.append((x, y+1, path+'D'))

        states = new_states

def part1(s):
    answer = shortest_path(s, 4, 4)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 17)
part1(INPUT)
part2(INPUT)
