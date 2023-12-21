import collections
import math

import lib.aoc

class Network:
    def __init__(self, s):
        self._connections = {}
        self._input_map = collections.defaultdict(list)

        for line in s.splitlines():
            name, outputs = line.split(' -> ')
            outputs = outputs.split(', ')

            if name == 'broadcaster':
                t = None
            else:
                t = name[0]
                name = name[1:]

            self._connections[name] = (t, outputs)

            for dest in outputs:
                self._input_map[dest].append(name)

        self._memory = {}

        for node, (t, _) in self._connections.items():
            if t is None:
                continue
            if t == '%':
                self._memory[node] = False
            elif t == '&':
                self._memory[node] = {d: False for d in self._input_map[node]}

    def press_button(self, modules_to_track=None):
        low, high = 0, 0

        todo = [(None, 'broadcaster', False)]

        # TODO: Very cludgy
        tracked_signals = []

        while todo:
            new_todo = []

            for src, node, is_high_pulse in todo:
                if is_high_pulse:
                    high += 1
                else:
                    low += 1

                # TODO: Very cludgy
                if modules_to_track is not None:
                    if node in modules_to_track and not is_high_pulse:
                        tracked_signals.append(node)

                info = self._connections.get(node)
                if info is None:
                    continue

                t, dests = info
                if t == '%':
                    if is_high_pulse:
                        continue
                    last_state = self._memory[node]
                    self._memory[node] = not last_state
                    for d in dests:
                        new_todo.append((node, d, not last_state))
                elif t == '&':
                    state = self._memory[node]
                    state[src] = is_high_pulse

                    # Send a high signal unless *all* inputs are high
                    out = sum(state.values()) < len(state)

                    for d in dests:
                        new_todo.append((node, d, out))
                elif t is None:
                    for d in dests:
                        new_todo.append((node, d, is_high_pulse))
                else:
                    assert(False)

            todo = new_todo

        if modules_to_track is not None:
            return tracked_signals

        return low, high

    def num_cycles_until_low_output(self):
        # Assumptions:
        # 1) There is a single output node
        # 2) That output node is fed by a single conjunction module
        # 3) That conjunction module is fed by n conjunction modules
        # 4) The broadcast node outputs to n modules
        # 5) Each of those outputs from broadcast links to a distinct
        # subtree which reaches one of the final conjuction modules
        # 6) Each subtree regularly outputs a low pulse after a set number of
        # button presses
        outputs = set(self._input_map) - set(self._connections)
        assert(len(outputs) == 1)

        output = list(outputs)[0]

        output_feeds = self._input_map[output]
        assert(len(output_feeds) == 1)

        # Must be fed a high signal to output a low signal
        output_feed = list(output_feeds)[0]
        assert(self._connections[output_feed][0] == '&')

        # These must be fed a low signal to output a high signal
        subtree_leaves = self._input_map[output_feed]
        assert(all(self._connections[leaf][0] == '&'
                   for leaf in subtree_leaves))

        subtree_cycles = {}
        cycle = 0

        while len(subtree_cycles) < len(subtree_leaves):
            cycle += 1

            # TODO: Very cludgy
            tracked_signals = self.press_button(subtree_leaves)

            for leaf in tracked_signals:
                if leaf in subtree_cycles:
                    continue
                subtree_cycles[leaf] = cycle

        return math.lcm(*subtree_cycles.values())

def part1(s):
    n = Network(s)

    low, high = 0, 0

    for _ in range(1000):
        d_low, d_high = n.press_button()
        low += d_low
        high += d_high

    answer = low * high

    lib.aoc.give_answer(2023, 20, 1, answer)

def part2(s):
    answer = Network(s).num_cycles_until_low_output()

    lib.aoc.give_answer(2023, 20, 2, answer)

INPUT = lib.aoc.get_input(2023, 20)
part1(INPUT)
part2(INPUT)
