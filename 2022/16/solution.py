import numpy

import lib.aoc

def find_best_pressures_per_valve_combo(s, total_time):
    valves = {}

    valves_with_flow = []
    valves_without_flow = []

    for line in s.splitlines():
        parts = line.split()
        valve = parts[1]
        flow_rate = int(parts[4][5:-1])
        leads_to = ''.join(parts[9:]).split(',')
        valves[valve] = (flow_rate, leads_to)

        if flow_rate == 0:
            valves_without_flow.append(valve)
        else:
            valves_with_flow.append(valve)

    valve_to_num = (valves_with_flow + valves_without_flow).index

    valves = {
        valve_to_num(valve): (flow_rate, tuple(map(valve_to_num, leads_to)))
        for valve, (flow_rate, leads_to) in valves.items()
    }

    good_valve_combos = 2 ** len(valves_with_flow)

    # Offset "active" states by 1 to differentiate them
    # This will be undone later on
    states = [numpy.zeros(good_valve_combos, dtype=int)
              for _ in range(len(valves))]
    states[valve_to_num('AA')][0] = 1

    for t in range(1, total_time+1):
        new_states = [numpy.zeros(good_valve_combos, dtype=int)
                      for _ in range(len(valves))]
        for loc, (locstates, new_locstates) in enumerate(zip(states,
                                                             new_states)):
            flow_rate, leads_to = valves[loc]

            if flow_rate > 0:
                # Open the valve
                loc_mask = 1 << loc

                unopened = (numpy.arange(good_valve_combos) & loc_mask) == 0
                condition = unopened & (locstates > 0)

                additional_flow = flow_rate * (total_time - t)
                new_pressure = locstates[condition] + additional_flow

                locs_to_adjust = condition.nonzero()[0] | loc_mask
                states_to_adjust = new_locstates[locs_to_adjust]

                # Due to slicing the adjusted array needs to be assigned rather
                # than adjusted in place
                new_locstates[locs_to_adjust] = numpy.maximum(states_to_adjust,
                                                              new_pressure)

            for dest in leads_to:
                # Movement
                numpy.maximum(new_states[dest], locstates,
                              out=new_states[dest])

        states = new_states

    best = numpy.zeros(good_valve_combos, dtype=int)
    for locstates in states:
        numpy.maximum(best, locstates,
                      out=best)

    # Remove the offset used above
    best -= 1

    return best[best > 0], numpy.nonzero(best > 0)[0]

def part1(s):
    answer = max(find_best_pressures_per_valve_combo(s, 30)[0])

    lib.aoc.give_answer(2022, 16, 1, answer)

def part2(s):
    pressures, valve_combos = find_best_pressures_per_valve_combo(s, 26)

    valid_pairs = (numpy.tile(valve_combos, len(valve_combos)) &
                   numpy.repeat(valve_combos, len(valve_combos))) == 0
    answer = numpy.amax(numpy.tile(pressures, len(pressures))[valid_pairs] +
                        numpy.repeat(pressures, len(pressures))[valid_pairs])

    lib.aoc.give_answer(2022, 16, 2, answer)

INPUT = lib.aoc.get_input(2022, 16)
part1(INPUT)
part2(INPUT)
