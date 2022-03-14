import lib.aoc

def parse_tree(s):
    def impl(packet):
        num_children = packet[0]
        num_metadata = packet[1]

        packet = packet[2:]

        children = []
        while num_children > 0:
            child, packet = impl(packet)
            children.append(child)
            num_children -= 1

        metadata = packet[:num_metadata]
        packet = packet[num_metadata:]

        return (children, metadata), packet

    packet = list(map(int, s.split()))

    root, rest = impl(packet)
    assert(len(rest) == 0)
    return root

def part1(s):
    root = parse_tree(s)

    def sum_metadata(node):
        children, metadata = node
        return sum(map(sum_metadata, children)) + sum(metadata)

    answer = sum_metadata(root)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 8)
part1(INPUT)
part2(INPUT)
