import lib.aoc
import lib.ocr

def parse_input(s):
    for line in s.splitlines():
        line = line.replace('=<', ' ').replace('>', ' ').replace(',', '')
        _, px, py, _, vx, vy = line.split()

        yield int(px), int(py), int(vx), int(vy)

def part1(s):
    points = []
    velocities = []

    for px, py, vx, vy in parse_input(s):
        points.append((px, py))
        velocities.append((vx, vy))

    while True:
        min_y = min(y for x,y in points)
        max_y = max(y for x,y in points)

        if max_y - min_y < 10:
            # Assume that the valid position is relatively short
            answer = lib.ocr.parse_coord_set(points)
            break

        for idx, ((px, py), (vx, vy)) in enumerate(zip(points, velocities)):
            points[idx] = (px+vx, py+vy)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 10)
part1(INPUT)
part2(INPUT)
