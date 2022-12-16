import lib.aoc

def parse_valves(s):
    valves = {}

    for line in s.splitlines():
        parts = line.split()
        valve = parts[1]
        flow_rate = int(parts[4][5:-1])
        lead_to = ''.join(parts[9:]).split(',')
        valves[valve] = (flow_rate, lead_to)

    return valves

def part1(s):
    valves = parse_valves(s)

    TOTAL_TIME = 30

    states = [('AA', set(), 0)]

    best = {}

    for t in range(1, TOTAL_TIME+1):
        print(t, len(states))

        new_states = []
        for loc, opened, pressure in states:
            key = (loc, ','.join(sorted(opened)))
            if key in best and pressure <= best[key]:
                continue

            best[key] = pressure

            flow_rate, lead_to = valves[loc]
            if loc not in opened and flow_rate > 0:
                new_states.append((loc, opened | {loc}, pressure + flow_rate * (TOTAL_TIME - t)))
            for dest in lead_to:
                new_states.append((dest, opened, pressure))

        states = new_states

    answer = max(pressure for _, _, pressure in states)

    lib.aoc.give_answer(2022, 16, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 16)
part1(INPUT)
part2(INPUT)
