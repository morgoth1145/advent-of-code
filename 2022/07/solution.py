import functools
import posixpath

import lib.aoc

def parse_input(s):
    folders = {}

    cwd = '~'

    lines = s.splitlines()
    while lines:
        line = lines.pop(0)
        assert(line[0] == '$')
        cmd = line[1:].strip()
        if cmd == 'ls':
            contents = []
            while lines:
                if lines[0][0] == '$':
                    break
                item = lines.pop(0)
                size, item = item.split(maxsplit=1)
                if size != 'dir':
                    size = int(size)
                contents.append((size, item))
            folders[cwd] = contents
        else:
            assert(cmd.startswith('cd '))
            rest = cmd[3:]
            if rest == '/':
                cwd = '/'
            elif rest == '..':
                cwd = posixpath.split(cwd)[0]
            else:
                cwd = posixpath.join(cwd, rest)

    return folders

def part1(s):
    folders = parse_input(s)

    @functools.cache
    def get_folder_size(name):
        contents = folders[name]
        dir_size = 0
        for size, item in contents:
            if size == 'dir':
                dir_size += get_folder_size(posixpath.join(name, item))
            else:
                dir_size += size
        return dir_size

    answer = 0

    for name in folders.keys():
        size = get_folder_size(name)
        if size <= 100000:
            answer += size

    lib.aoc.give_answer(2022, 7, 1, answer)

def part2(s):
    folders = parse_input(s)

    @functools.cache
    def get_folder_size(name):
        contents = folders[name]
        dir_size = 0
        for size, item in contents:
            if size == 'dir':
                dir_size += get_folder_size(posixpath.join(name, item))
            else:
                dir_size += size
        return dir_size

    TOT_SPACE = 70000000
    REQUIRED_FREE = 30000000
    USED = get_folder_size('/')
    UNUSED = TOT_SPACE - USED
    TO_FREE = REQUIRED_FREE - UNUSED

    answer = min(get_folder_size(name)
                 for name in folders.keys()
                 if get_folder_size(name) >= TO_FREE)

    lib.aoc.give_answer(2022, 7, 2, answer)

INPUT = lib.aoc.get_input(2022, 7)
part1(INPUT)
part2(INPUT)
