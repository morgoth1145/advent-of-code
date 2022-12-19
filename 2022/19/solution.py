import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        parts = line.split()
        yield (int(parts[1][:-1]), int(parts[6]), int(parts[12]),
               int(parts[18]), int(parts[21]), int(parts[27]), int(parts[30]))

def blueprint_quality(blueprint, minutes):
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

    for t in range(minutes):
        new_states = set()

        for state in states:
            (ore_robots, ore,
             clay_robots, clay,
             obsidian_robots, obsidian,
             geode_robots, geodes) = state

            new_states.add((ore_robots, ore + ore_robots,
                            clay_robots, clay + clay_robots,
                            obsidian_robots, obsidian + obsidian_robots,
                            geode_robots, geodes + geode_robots))
            if ore >= ore_ore_cost:
                new_states.add((ore_robots + 1, ore - ore_ore_cost + ore_robots,
                                clay_robots, clay + clay_robots,
                                obsidian_robots, obsidian + obsidian_robots,
                                geode_robots, geodes + geode_robots))
            if ore >= clay_ore_cost:
                new_states.add((ore_robots, ore - clay_ore_cost + ore_robots,
                                clay_robots + 1, clay + clay_robots,
                                obsidian_robots, obsidian + obsidian_robots,
                                geode_robots, geodes + geode_robots))
            if ore >= obsidian_ore_cost and clay >= obsidian_clay_cost:
                new_states.add((ore_robots, ore - obsidian_ore_cost + ore_robots,
                                clay_robots, clay - obsidian_clay_cost + clay_robots,
                                obsidian_robots + 1, obsidian + obsidian_robots,
                                geode_robots, geodes + geode_robots))
            if ore >= geode_ore_cost and obsidian >= geode_obsidian_cost:
                new_states.add((ore_robots, ore - geode_ore_cost + ore_robots,
                                clay_robots, clay + clay_robots,
                                obsidian_robots, obsidian - geode_obsidian_cost + obsidian_robots,
                                geode_robots + 1, geodes + geode_robots))

        states = new_states

    max_geodes = max(s[-1] for s in states)

    return max_geodes * num

# Horrible brute force solution which requires lots of parallel processes!
def part1(s):
    data = list(parse_input(s))

    import multiprocessing

    with multiprocessing.Pool(processes=len(data)) as pool:
        results = []
        for bp in data:
            results.append(pool.apply_async(blueprint_quality, (bp, 24)))

        answer = 0
        for i, r in enumerate(results):
            score = r.get()
            answer += score
            print(f'{i} done with score {score}')

    lib.aoc.give_answer(2022, 19, 1, answer)

def part2(s):
    pass

if __name__ == '__main__':
    INPUT = lib.aoc.get_input(2022, 19)
    part1(INPUT)
    part2(INPUT)
