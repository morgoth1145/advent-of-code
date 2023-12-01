import lib.aoc

def find_first_num(line, mapping, reverse_key):
    best = None
    best_idx = len(line)

    for search, d in mapping.items():
        if reverse_key:
            search = search[::-1]
        if search in line:
            idx = line.index(search)
            if idx < best_idx:
                best_idx = idx
                best = d

    return best

def find_calibration_value(line, mapping):
    return (find_first_num(line, mapping, False) * 10 +
            find_first_num(line[::-1], mapping, True))

def make_mapping(digit_sequence):
    mapping = {}
    for d, c in enumerate(digit_sequence):
        mapping[c] = d
    return mapping

def part1(s):
    mapping = make_mapping('0123456789')

    answer = sum(find_calibration_value(line, mapping)
                 for line in s.splitlines())

    lib.aoc.give_answer(2023, 1, 1, answer)

def part2(s):
    mapping = make_mapping('0123456789')
    mapping |= make_mapping(('zero', 'one',
                             'two', 'three',
                             'four', 'five',
                             'six', 'seven',
                             'eight', 'nine'))

    answer = sum(find_calibration_value(line, mapping)
                 for line in s.splitlines())

    lib.aoc.give_answer(2023, 1, 2, answer)

INPUT = lib.aoc.get_input(2023, 1)
part1(INPUT)
part2(INPUT)
