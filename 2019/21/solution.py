import lib.aoc

intcode = __import__('2019.intcode').intcode

def run_springdroid(s, springscript):
    in_chan, out_chan = intcode.Program(s).run()

    for c in springscript:
        in_chan.send(ord(c))

    for c in out_chan:
        if c < 256:
            print(chr(c), end='')
        else:
            return c

def part1(s):
    answer = run_springdroid(s, '''NOT A J
OR B T
AND C T
NOT T T
AND D T
OR T J
WALK
''')

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = run_springdroid(s, '''OR E J
AND I J
OR H J
AND D J
OR B T
AND C T
NOT T T
AND T J
NOT A T
OR T J
RUN
''')

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 21)
part1(INPUT)
part2(INPUT)
