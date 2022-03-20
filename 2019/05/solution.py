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
    pass

INPUT = lib.aoc.get_input(2019, 5)
part1(INPUT)
part2(INPUT)
