import lib.aoc

intcode = __import__('2019.intcode').intcode

def part1(s):
    p = intcode.Program(s)

    p.run_async()
    p.in_chan.send(1)

    answer = None

    for val in p.out_chan:
        answer = val

    print(f'The answer to part one is {answer}')

def part2(s):
    p = intcode.Program(s)

    p.run_async()
    p.in_chan.send(5)

    answer = p.out_chan.recv()

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 5)
part1(INPUT)
part2(INPUT)
