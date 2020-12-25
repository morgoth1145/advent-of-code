import helpers.input

def part1(s):
    a, b = map(int, s.splitlines())

    cracking_val = 1
    encrypt_a = 1
    encrypt_b = 1
    while True:
        if cracking_val == a:
            answer = encrypt_b
            break
        if cracking_val == b:
            answer = encrypt_a
            break
        cracking_val = (cracking_val * 7) % 20201227
        encrypt_a = (encrypt_a * a) % 20201227
        encrypt_b = (encrypt_b * b) % 20201227

    print(f'The answer to part one is {answer}')

def part2(s):
    print('There is no part two for Christmas!')

INPUT = helpers.input.get_input(2020, 25)

part1(INPUT)
part2(INPUT)
