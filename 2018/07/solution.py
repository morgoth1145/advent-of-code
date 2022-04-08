import collections

import lib.aoc

def parse_input(s):
    dep_graph = collections.defaultdict(set)
    all_steps = set()

    for line in s.splitlines():
        _, a, _, _, _, _, _, b, _, _ = line.split()
        dep_graph[b].add(a)
        all_steps.add(b)
        all_steps.add(a)

    return dep_graph, sorted(all_steps)

def best_next_step(all_steps, dep_graph, steps_started, steps_done):
    for step in all_steps:
        if step in steps_started:
            continue
        if len(dep_graph[step] - steps_done) == 0:
            # We can do this now!
            return step

def part1(s):
    dep_graph, all_steps = parse_input(s)

    done = set()
    order = []

    while len(order) < len(all_steps):
        step = best_next_step(all_steps, dep_graph, done, done)
        order.append(step)
        done.add(step)

    answer = ''.join(order)

    lib.aoc.give_answer(2018, 7, 1, answer)

def part2(s):
    dep_graph, all_steps = parse_input(s)

    done = set()
    started = set()
    workers = [None] * 5

    answer = -1 # Start on second 0

    while len(done) < len(all_steps):
        answer += 1
        for idx, processing in enumerate(workers):
            if processing is None:
                continue
            step, remaining = processing
            remaining -= 1
            if remaining == 0:
                done.add(step)
                workers[idx] = None
            else:
                workers[idx] = (step, remaining)

        for idx, processing in enumerate(workers):
            if processing is not None:
                continue

            step = best_next_step(all_steps, dep_graph, started, done)
            if step is None:
                # No worker can start something new right now
                break

            workers[idx] = (step, 60 + ord(step) - ord('A') + 1)
            started.add(step)

    lib.aoc.give_answer(2018, 7, 2, answer)

INPUT = lib.aoc.get_input(2018, 7)
part1(INPUT)
part2(INPUT)
