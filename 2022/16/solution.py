import itertools

import lib.aoc
import lib.graph

def parse_valves(s):
    valves = {}

    for line in s.splitlines():
        parts = line.split()
        valve = parts[1]
        flow_rate = int(parts[4][5:-1])
        lead_to = ''.join(parts[9:]).split(',')
        valves[valve] = (flow_rate, lead_to)

    valve_to_num = {}
    for key in sorted(valves.keys()):
        valve_to_num[key] = 1 << len(valve_to_num)

    valves = {
        valve_to_num[valve]: (flow_rate, tuple(map(valve_to_num.get, lead_to)))
        for valve, (flow_rate, lead_to) in valves.items()
    }

    return valves, valve_to_num

def part1(s):
    valves, valve_to_num = parse_valves(s)

    TOTAL_TIME = 30

    states = [(valve_to_num['AA'], 0, 0)]

    best = {}

    for t in range(1, TOTAL_TIME+1):
        print(t, len(states))

        new_states = []
        for loc, opened, pressure in states:
            key = (loc, opened)
            if key in best and pressure <= best[key]:
                continue

            best[key] = pressure

            flow_rate, lead_to = valves[loc]
            if loc & opened == 0 and flow_rate > 0:
                new_states.append((loc, opened | loc, pressure + flow_rate * (TOTAL_TIME - t)))
            for dest in lead_to:
                new_states.append((dest, opened, pressure))

        states = new_states

    answer = max(pressure for _, _, pressure in states)

    lib.aoc.give_answer(2022, 16, 1, answer)

# This is abysmally slow. But it works.
# BFS was bogging down my memory, so I inverted this to a graph search for
# the least amount of *wasted* pressure. (AKA, pressure that could have been
# released had all the valves been open from the start.)
def part2(s):
    valves, valve_to_num = parse_valves(s)

    ALL_VALVES = 0
    for valve in valves.keys():
        assert(ALL_VALVES & valve == 0)
        ALL_VALVES = ALL_VALVES | valve

    TOTAL_TIME = 26

    MAXIMUM_FLOW_PER_TICK = 0
    for flow_rate, _ in valves.values():
        MAXIMUM_FLOW_PER_TICK += flow_rate

    TOTAL_MAXIMUM_FLOW = MAXIMUM_FLOW_PER_TICK * TOTAL_TIME

    def calc_sub_states(loc, opened):
        flow_rate, lead_to = valves[loc]
        if loc & opened == 0 and flow_rate > 0:
            yield loc, loc, flow_rate
        for dest in lead_to:
            yield dest, None, 0

    best_seen_time = TOTAL_TIME+1

    def neighbor_fn(state):
        self, elephant, opened, current_flow, time_remaining = state
        assert(time_remaining > 0)

        nonlocal best_seen_time
        if best_seen_time > time_remaining:
            print(time_remaining)
            best_seen_time = time_remaining

        if opened == ALL_VALVES:
            yield (None, None, opened, current_flow, time_remaining-1), 0
            return

        self_moves = list(calc_sub_states(self, opened))
        elephant_moves = list(calc_sub_states(elephant, opened))

        for ((dest1, open1, new_flow_1),
             (dest2, open2, new_flow_2)) in itertools.product(self_moves,
                                                              elephant_moves):
            if open1 is not None and open2 is not None and open1 == open2:
                continue
            new_opened = opened
            if open1 is not None:
                new_opened |= open1
            if open2 is not None:
                new_opened |= open2

            new_flow = current_flow + new_flow_1 + new_flow_2
            yield (dest1, dest2, new_opened, new_flow, time_remaining-1), MAXIMUM_FLOW_PER_TICK - current_flow

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    start = (valve_to_num['AA'], valve_to_num['AA'], 0, 0, TOTAL_TIME)

    def end_fn(state):
        return state[-1] == 0

    least_missed_flow = lib.graph.dijkstra_length_fuzzy_end(graph, start, end_fn)

    answer = TOTAL_MAXIMUM_FLOW - least_missed_flow

    lib.aoc.give_answer(2022, 16, 2, answer)

INPUT = lib.aoc.get_input(2022, 16)
part1(INPUT)
part2(INPUT)
