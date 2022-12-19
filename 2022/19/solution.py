import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        parts = line.split()
        yield (int(parts[1][:-1]), int(parts[6]), int(parts[12]),
               int(parts[18]), int(parts[21]), int(parts[27]), int(parts[30]))

def tri(n):
    return n * (n+1) // 2

def max_geodes(blueprint, minutes):
    (num,
     ore_ore_cost,
     clay_ore_cost,
     obsidian_ore_cost, obsidian_clay_cost,
     geode_ore_cost, geode_obsidian_cost) = blueprint

    # Ignore the cost of ore robots as once we have enough we don't need
    # to build more!
    max_ore_cost = max(clay_ore_cost, obsidian_ore_cost, geode_ore_cost)

    states = [(1, 0,
               0, 0,
               0, 0,
               0, 0)]

    min_guaranteed = 0

    for t in range(minutes):
        new_states = set()

        for state in states:
            (ore_robots, ore,
             clay_robots, clay,
             obsidian_robots, obsidian,
             geode_robots, geodes) = state

            rem_minutes = minutes - t
            guaranteed = geodes + geode_robots * rem_minutes
            min_guaranteed = max(min_guaranteed, guaranteed)
            upper_limit = guaranteed + tri(max(rem_minutes-1, 0))
            if upper_limit <= min_guaranteed:
                # This branch cannot possibly make more geodes than our minimum
                continue

            robot_options = 0
            if ore_robots < max_ore_cost:
                if ore >= ore_ore_cost:
                    robot_options += 1
                    new_states.add((ore_robots + 1, ore - ore_ore_cost + ore_robots,
                                    clay_robots, clay + clay_robots,
                                    obsidian_robots, obsidian + obsidian_robots,
                                    geode_robots, geodes + geode_robots))
            else:
                # We have enough ore robots!
                robot_options += 1

            if ore >= clay_ore_cost:
                robot_options += 1
                new_states.add((ore_robots, ore - clay_ore_cost + ore_robots,
                                clay_robots + 1, clay + clay_robots,
                                obsidian_robots, obsidian + obsidian_robots,
                                geode_robots, geodes + geode_robots))

            if ore >= obsidian_ore_cost and clay >= obsidian_clay_cost:
                robot_options += 1
                new_states.add((ore_robots, ore - obsidian_ore_cost + ore_robots,
                                clay_robots, clay - obsidian_clay_cost + clay_robots,
                                obsidian_robots + 1, obsidian + obsidian_robots,
                                geode_robots, geodes + geode_robots))
            elif clay_robots == 0:
                # We don't get clay, ignore this option!
                robot_options += 1

            if ore >= geode_ore_cost and obsidian >= geode_obsidian_cost:
                robot_options += 1
                new_states.add((ore_robots, ore - geode_ore_cost + ore_robots,
                                clay_robots, clay + clay_robots,
                                obsidian_robots, obsidian - geode_obsidian_cost + obsidian_robots,
                                geode_robots + 1, geodes + geode_robots))
            elif obsidian_robots == 0:
                # We don't get obsidian, ignore this option!
                robot_options += 1

            if robot_options < 4:
                # Always make a robot if we can make any of the four
                new_states.add((ore_robots, ore + ore_robots,
                                clay_robots, clay + clay_robots,
                                obsidian_robots, obsidian + obsidian_robots,
                                geode_robots, geodes + geode_robots))

        states = new_states

    return min_guaranteed

def part1(s):
    answer = 0

    for i, bp in enumerate(parse_input(s)):
        answer += (i+1) * max_geodes(bp, 24)

    lib.aoc.give_answer(2022, 19, 1, answer)

def part2(s):
    answer = 1

    for bp in list(parse_input(s))[:3]:
        answer *= max_geodes(bp, 32)

    lib.aoc.give_answer(2022, 19, 2, answer)

INPUT = lib.aoc.get_input(2022, 19)
part1(INPUT)
part2(INPUT)
