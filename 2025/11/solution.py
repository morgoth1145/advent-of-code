import collections
import functools

import lib.aoc

def parse_input(s):
    g = {}

    for line in s.splitlines():
        a, b = line.split(': ')
        g[a] = set(b.split())

    return g

def part1(s):
    g = parse_input(s)

    @functools.cache
    def count_paths(pos, seen):
        if pos == 'out':
            return 1

        seen = set(seen)

        total = 0
        for n in g[pos]:
            if n in seen:
                continue
            seen.add(n)
            total += count_paths(n, tuple(sorted(seen)))
            seen.remove(n)

        return total

    answer = count_paths('you', tuple())

    lib.aoc.give_answer(2025, 11, 1, answer)

def part2(s):
    g = parse_input(s)

    inv_g = collections.defaultdict(set)

    for pos, neighbors in g.items():
        for n in neighbors:
            inv_g[n].add(pos)

    def count_path_wrap(start, dest, forbidden):
        todo = [dest]
        can_reach_dest = set(todo)
        while todo:
            pos = todo.pop()
            for n in inv_g[pos]:
                if n in can_reach_dest or n in forbidden:
                    continue
                can_reach_dest.add(n)
                todo.append(n)

        use_g = collections.defaultdict(set)

        for pos, neighbors in g.items():
            if pos not in can_reach_dest:
                continue
            use_g[pos] = [n for n in neighbors if n in can_reach_dest]

        @functools.cache
        def count_paths(pos, seen):
            if pos == dest:
                return 1

            seen = set(seen)

            total = 0
            for n in use_g[pos]:
                if n in seen or n in forbidden:
                    continue
                seen.add(n)
                total += count_paths(n, tuple(sorted(seen)))
                seen.remove(n)

            return total

        return count_paths(start, tuple())

    answer = 0

    dac_to_out = count_path_wrap('dac', 'out', {'fft', 'srv'})
    srv_to_fft = count_path_wrap('svr', 'fft', {'out', 'dac'})
    fft_to_dac = count_path_wrap('fft', 'dac', {'out', 'srv'})

    answer += srv_to_fft * fft_to_dac * dac_to_out

    # Not possible with my input
##    srv_to_dac = count_path_wrap('svr', 'dac', {'out', 'fft'})
##    fft_to_out = count_path_wrap('fft', 'out', {'dac', 'srv'})
##    dac_to_fft = count_path_wrap('dac', 'fft', {'out', 'srv'})
##
##    answer += srv_to_dac * dac_to_fft * fft_to_out

    lib.aoc.give_answer(2025, 11, 2, answer)

INPUT = lib.aoc.get_input(2025, 11)
part1(INPUT)
part2(INPUT)
