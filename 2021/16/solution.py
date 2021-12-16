import lib.aoc

def parse_impl(bits):
    v = bits[:3]
    bits = bits[3:]
    v = int(v, base=2)
    t = bits[:3]
    bits = bits[3:]
    t = int(t, base=2)
    if t == 4:
        # Literal
        parts = ''
        while True:
            p = bits[:5]
            bits = bits[5:]
            parts += p[1:]
            if p[0] == '0':
                break
        n = int(parts, base=2)
        packet = (v, t, n)
        return packet, bits
    i = bits[0]
    bits = bits[1:]
    if i == '0':
        l = bits[:15]
        bits = bits[15:]
        sub_len = int(l, 2)
        sub = []
        sub_bits = bits[:sub_len]
        bits = bits[sub_len:]
        while sub_bits:
            s, sub_bits = parse_impl(sub_bits)
            sub.append(s)
    else:
        l = bits[:11]
        bits = bits[11:]
        sub = []
        for _ in range(int(l, base=2)):
            s, bits = parse_impl(bits)
            sub.append(s)

    packet = (v, t, i, l, sub)
    return packet, bits

def parse(s):
    bits = []
    for n in [int(n, base=16) for n in s]:
        b = bin(n)[2:]
        while len(b) < 4:
            b = '0' + b
        bits.extend(list(b))
    bits = ''.join(bits)
    return parse_impl(bits)[0]

def part1(s):
    packet = parse(s)

    to_handle = [packet]

    answer = 0

    while to_handle:
        p = to_handle.pop(0)
        answer += p[0]
        if p[1] == 4:
            # Literal
            continue
        to_handle.extend(p[4])

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 16)
part1(INPUT)
part2(INPUT)
