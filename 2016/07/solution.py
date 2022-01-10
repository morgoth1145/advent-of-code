import lib.aoc

def has_abba(sequence):
    for a, b, c, d in zip(sequence,
                          sequence[1:],
                          sequence[2:],
                          sequence[3:]):
        if a == d and b == c and a != b:
            return True

    return False

def is_valid(ip):
    norm_sequences = []
    hypernets = []

    while True:
        idx = ip.find('[')
        if idx == -1:
            assert(-1 == ip.find(']'))
            norm_sequences.append(ip)
            break

        end_idx = ip.find(']')
        assert(end_idx > idx)

        norm_sequences.append(ip[:idx])
        hyper = ip[idx+1:end_idx]
        ip = ip[end_idx+1:]
        assert(hyper.find('[') == -1)
        hypernets.append(hyper)

    return not any(filter(has_abba, hypernets)) and any(filter(has_abba, norm_sequences))

def part1(s):
    answer = len(list(filter(is_valid, s.splitlines())))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 7)
part1(INPUT)
part2(INPUT)
