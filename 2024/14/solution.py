import lib.aoc

class Robots:
    def __init__(self, s, width, height):
        self.robots = []
        for line in s.splitlines():
            p, v = line.split()
            p = tuple(map(int, p[2:].split(',')))
            v = tuple(map(int, v[2:].split(',')))
            self.robots.append([p, v])

        self.width = width
        self.height = height

    def step(self):
        for robot in self.robots:
            (px, py), (vx, vy) = robot
            px = (px + vx) % self.width
            py = (py + vy) % self.height
            robot[0] = (px, py)

    @property
    def safety_factor(self):
        quadrants = {(qx, qy): 0
                     for qx in (0, 1)
                     for qy in (0, 1)}

        middle_x = self.width//2
        middle_y = self.height//2

        for (px, py), _ in self.robots:
            if px == middle_x or py == middle_y:
                continue

            qx = px > middle_x
            qy = py > middle_y
            quadrants[qx,qy] += 1

        safety = 1
        for v in quadrants.values():
            safety *= v

        return safety

    @property
    def robot_state_key(self):
        return [p for p, v in self.robots]

    @property
    def cluster_factor(self):
        robot_positions = set(p for p, v in self.robots)

        clustering = 0

        for (px, py), _ in self.robots:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 == dy:
                        continue
                    if (px+dx, py+dy) in robot_positions:
                        clustering += 1

        return clustering

def part1(s):
    robots = Robots(s, 101, 103)

    for _ in range(100):
        robots.step()

    answer = robots.safety_factor

    lib.aoc.give_answer(2024, 14, 1, answer)

def part2(s):
    robots = Robots(s, 101, 103)

    start_state = robots.robot_state_key

    t = 0

    best = None

    while t == 0 or start_state != robots.robot_state_key:
        clustering = robots.cluster_factor
        if best is None or clustering > best[0]:
            best = (clustering, t)

        t += 1
        robots.step()

    answer = best[1]

    lib.aoc.give_answer(2024, 14, 2, answer)

INPUT = lib.aoc.get_input(2024, 14)
part1(INPUT)
part2(INPUT)
