import lib.aoc
import lib.ocr

def parse(s):
    points = []
    velocities = []

    for line in s.splitlines():
        line = line.replace('=<', ' ').replace('>', ' ').replace(',', '')
        _, px, py, _, vx, vy = line.split()

        points.append((int(px), int(py)))
        velocities.append((int(vx), int(vy)))

    steps = 0

    while True:
        min_y = min(y for x,y in points)
        max_y = max(y for x,y in points)

        if max_y - min_y < 10:
            # Assume that the valid position is relatively short
            return lib.ocr.parse_coord_set(points), steps

        for idx, ((px, py), (vx, vy)) in enumerate(zip(points, velocities)):
            points[idx] = (px+vx, py+vy)
        steps += 1

def part1(s):
    answer, _ = parse(s)

    print(f'The answer to part one is {answer}')

def part2(s):
    _, answer = parse(s)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 10)
part1(INPUT)
part2(INPUT)
