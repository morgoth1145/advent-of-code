import lib.aoc

intcode = __import__('2019.intcode').intcode

def play_text_adventure(s, initial_commands):
    initial_commands = initial_commands.split('\n')
    in_chan, out_chan = intcode.Program(s).run()

    line = ''

    for c in map(chr, out_chan):
        if c == '\n':
            print(line)
            if line == 'Command?':
                if initial_commands:
                    command = initial_commands.pop(0)
                    print(command)
                else:
                    command = input()
                for c in command:
                    in_chan.send(ord(c))
                in_chan.send(ord('\n'))
            line = ''
            continue
        line += c

def run_text_adventure(s, initial_commands, direction_to_security, inventory):
    if initial_commands[-1] != '\n':
        initial_commands += '\n'

    security_cracking = ''

    old_mask = 2 ** len(inventory) - 1

    for mask in range(2 ** len(inventory)):
        MASK_SAVE = mask
        for obj in inventory:
            if (mask & 1) != (old_mask & 1):
                if old_mask & 1:
                    security_cracking += 'drop ' + obj + '\n'
                else:
                    security_cracking += 'take ' + obj + '\n'
            mask >>= 1
            old_mask >>= 1
        security_cracking += direction_to_security + '\n'
        old_mask = MASK_SAVE

    play_text_adventure(s, initial_commands + security_cracking)

def part1(s):
    initial_commands = '''<INITIAL_COMMANDS_HERE>
'''
    direction_to_security = '<direction_to_security>'
    inventory = []

    run_text_adventure(s, initial_commands, direction_to_security, inventory)

    answer = int(input('What was the password? '))

    print(f'The answer to part one is {answer}')

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2019, 25)
part1(INPUT)
part2(INPUT)
