import lib.aoc

intcode = __import__('2019.intcode').intcode

def part1(s):
    p = intcode.Program(s)

    p.memory[1] = 12
    p.memory[2] = 2

    _, out = p.run()
    out.wait_for_close()

    answer = p.memory[0]

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = None

    for noun in range(100):
        for verb in range(100):
            p = intcode.Program(s)

            p.memory[1] = noun
            p.memory[2] = verb

            _, out = p.run()
            out.wait_for_close()

            if p.memory[0] == 19690720:
                answer = 100 * noun + verb
                break

        if answer is not None:
            break

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 2)
part1(INPUT)
part2(INPUT)
