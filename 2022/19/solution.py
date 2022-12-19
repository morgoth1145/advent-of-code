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

    max_ore_cost = max(ore_ore_cost, clay_ore_cost, obsidian_ore_cost, geode_ore_cost)

    states = [(1, 0,
               0, 0,
               0, 0,
               0, 0)]

    min_guaranteed = 0

    for t in range(minutes):
        print(num, t, len(states))
        new_states = set()

        for state in states:
            (ore_robots, ore,
             clay_robots, clay,
             obsidian_robots, obsidian,
             geode_robots, geodes) = state

            rem_minutes = minutes - t
            guaranteed = geodes + geode_robots * rem_minutes
            min_guaranteed = max(min_guaranteed, guaranteed)
            if ore >= obsidian_ore_cost and clay >= obsidian_clay_cost:
                upper_limit = guaranteed + tri(max(rem_minutes-1, 0))
            else:
                upper_limit = guaranteed + tri(max(rem_minutes-2, 0))
            if upper_limit < min_guaranteed:
                continue

            robot_options = 0
            if ore >= ore_ore_cost:
                robot_options += 1
                new_states.add((ore_robots + 1, ore - ore_ore_cost + ore_robots,
                                clay_robots, clay + clay_robots,
                                obsidian_robots, obsidian + obsidian_robots,
                                geode_robots, geodes + geode_robots))
            if ore >= clay_ore_cost:
                robot_options += 1
                new_states.add((ore_robots, ore - clay_ore_cost + ore_robots,
                                clay_robots + 1, clay + clay_robots,
                                obsidian_robots, obsidian + obsidian_robots,
                                geode_robots, geodes + geode_robots))
            elif ore_robots < 2:
                # We probably need more ore robots
                robot_options += 1
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
                # Always make a robot if we can make all 4
                new_states.add((ore_robots, ore + ore_robots,
                                clay_robots, clay + clay_robots,
                                obsidian_robots, obsidian + obsidian_robots,
                                geode_robots, geodes + geode_robots))

        states = new_states

    max_geodes = max(s[-1] for s in states)

    return max_geodes

# Horrible brute force solution which requires lots of parallel processes!
def part1(s):
    data = list(parse_input(s))

    import multiprocessing

    with multiprocessing.Pool(processes=len(data)) as pool:
        results = []
        for bp in data:
            results.append(pool.apply_async(max_geodes, (bp, 24)))

        answer = 0
        for i, r in enumerate(results):
            geodes = r.get()
            answer += (i+1) * geodes
            print(f'{i} done with {geodes} geodes (score {(i+1) * geodes})')

    lib.aoc.give_answer(2022, 19, 1, answer)

def part2(s):
    data = list(parse_input(s))

    answer = 1

    # Horrible brute force solution!
    for i, bp in enumerate(data[:3]):
        geodes = max_geodes(bp, 32)
        print(f'Geodes for {i}: {geodes}')
        answer *= geodes

    lib.aoc.give_answer(2022, 19, 2, answer)

if __name__ == '__main__':
    INPUT = lib.aoc.get_input(2022, 19)
    part1(INPUT)
    part2(INPUT)
