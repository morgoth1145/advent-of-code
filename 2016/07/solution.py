import lib.aoc

def split_ip(ip):
    supernets = []
    hypernets = []

    while True:
        idx = ip.find('[')
        if idx == -1:
            assert(-1 == ip.find(']'))
            supernets.append(ip)
            break

        end_idx = ip.find(']')
        assert(end_idx > idx)

        supernets.append(ip[:idx])
        hyper = ip[idx+1:end_idx]
        ip = ip[end_idx+1:]
        assert(hyper.find('[') == -1)
        hypernets.append(hyper)

    return supernets, hypernets

def has_abba(sequence):
    for a, b, c, d in zip(sequence,
                          sequence[1:],
                          sequence[2:],
                          sequence[3:]):
        if a == d and b == c and a != b:
            return True

    return False

def supports_tls(ip):
    supernets, hypernets = split_ip(ip)

    if any(filter(has_abba, hypernets)):
        return False

    return any(filter(has_abba, supernets))

def part1(s):
    answer = len(list(filter(supports_tls, s.splitlines())))

    print(f'The answer to part one is {answer}')

def supports_ssl(ip):
    supernets, hypernets = split_ip(ip)

    for sequence in supernets:
        for a, b, c in zip(sequence,
                           sequence[1:],
                           sequence[2:]):
            if a == c and a != b:
                bab = b + a + b
                if any(bab in hyper_s
                       for hyper_s in hypernets):
                    return True

    return False

def part2(s):
    answer = len(list(filter(supports_ssl, s.splitlines())))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 7)
part1(INPUT)
part2(INPUT)
