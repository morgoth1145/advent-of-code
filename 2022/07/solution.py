import collections

import lib.aoc

def get_folder_sizes(s):
    folders = collections.defaultdict(int)

    cwd = []

    for line in s.splitlines():
        parts = line.split()
        if parts[0] == '$':
            if parts[1] == 'cd':
                if parts[2] == '..':
                    cwd.pop()
                elif parts[2] == '/':
                    # Special handling to avoid double slash
                    cwd = ['']
                else:
                    cwd.append(parts[2])
            elif parts[1] == 'ls':
                pass
            else:
                assert(False)
        elif parts[0] == 'dir':
            pass # Handled implicitly when adding up sizes
        else:
            size = int(parts[0])
            name = ''
            for fold in cwd:
                if name != '/':
                    # Special handling to avoid double slash
                    name += '/'
                name += fold
                folders[name] += size

    return folders

def part1(s):
    answer = sum(size
                 for size in get_folder_sizes(s).values()
                 if size <= 100000)

    lib.aoc.give_answer(2022, 7, 1, answer)

def part2(s):
    folders = get_folder_sizes(s)

    TO_FREE = 30000000 - (70000000 - folders['/'])

    answer = min(size
                 for size in folders.values()
                 if size >= TO_FREE)

    lib.aoc.give_answer(2022, 7, 2, answer)

INPUT = lib.aoc.get_input(2022, 7)
part1(INPUT)
part2(INPUT)
