import collections
import gmpy2
import re

import lib.aoc

intcode = __import__('2019.intcode').intcode

def run_text_adventure(s):
    # Any larger than this is some sort of infinite loop
    MAX_BLOCK_SIZE = 5000

    in_chan = lib.channels.SyncChannel()
    out_chan = lib.channels.BufferedChannel(MAX_BLOCK_SIZE)

    intcode.Program(s).run(in_chan=in_chan, out_chan=out_chan,
                           stop_on_no_input=True, stop_on_closed_output=True)

    block = ''

    for c in map(chr, out_chan):
        if c == '\n':
            if block.endswith('Command?'):
                command = yield block, True

                if command == 'terminate':
                    # Special command, terminate the adventure
                    break

                for c in command:
                    in_chan.send(ord(c))
                in_chan.send(ord('\n'))

                block = ''
                continue

        block += c

        if len(block) > MAX_BLOCK_SIZE:
            # This is too big, shut it down
            break

    in_chan.close()
    out_chan.close()

    yield block.rstrip(), False

def play_text_adventure(s):
    adventure = run_text_adventure(s)

    block, requesting_command = next(adventure)
    print(block)

    while requesting_command:
        block, requesting_command = adventure.send(input())
        print(block)

def parse_list(block):
    lines = block.split('\n')
    desc = lines[0].rstrip(':')

    l = []
    for item in lines[1:]:
        assert(item.startswith('- '))
        l.append(item[2:])

    return desc, l

def parse_room_block(block):
    parts = block.strip().split('\n\n')
    assert(parts[-1] == 'Command?')

    room = {}

    m = re.match('== (.*) ==', parts[0].split('\n')[0])
    room['name'] = m.group(1)

    for desc, l in map(parse_list, parts[1:-1]):
        if desc == 'Doors here lead':
            room['doors'] = l
        elif desc == 'Items here':
            room['items'] = l
        else:
            print(f'Unknown list description: {desc}')
            assert(False)

    return room

def parse_inventory(block):
    parts = block.strip().split('\n\n')
    assert(parts[-1] == 'Command?')

    assert(len(parts) == 2)
    if parts[0] == 'You aren\'t carrying any items.':
        return []

    desc, inv = parse_list(parts[0])
    assert(desc == 'Items in your inventory')

    return inv

def find_command_sequence(rooms, connections,
                          start_room, start_inv,
                          end_room, end_inv):
    # Only ever pick up items. Dropping items is a waste of commands
    end_inv = set(end_inv) | set(start_inv)
    required_pickups = end_inv - set(start_inv)

    start = (start_room, tuple(sorted(start_inv)))
    end = (end_room, tuple(sorted(end_inv)))

    seen = {start}

    # All state, sequence options for the current search
    options = [(start, [])]

    while options:
        new_options = []

        for state, sequence in options:
            if state == end:
                return sequence

            room, inv = state

            items_to_pick_up = set(rooms[room].get('items', [])) & required_pickups
            items_to_pick_up -= set(inv)

            if items_to_pick_up:
                # This room has a required pick up!
                next_item = min(items_to_pick_up)

                new_inv = tuple(sorted(inv + (next_item,)))
                new_state = (room, new_inv)
                if new_state in seen:
                    continue

                seen.add(new_state)
                new_options.append((new_state, sequence + ['take ' + next_item]))
                continue

            for door in rooms[room]['doors']:
                new_room = connections[room].get(door)
                if new_room is None:
                    # Not explored yet
                    continue

                new_state = (new_room, inv)
                if new_state in seen:
                    continue

                seen.add(new_state)
                new_options.append((new_state, sequence + [door]))

        options = new_options

    # No such sequence exists!
    return None

def solve_text_adventure(s):
    REVERSE_DIRECTIONS = {
        'north': 'south',
        'south': 'north',
        'east': 'west',
        'west': 'east',
    }

    SECURITY = 'Security Checkpoint'
    VALIDATION = 'Pressure-Sensitive Floor'

    adventure = None

    block = None
    requesting_command = False

    def restart(target_room):
        nonlocal adventure, block, requesting_command
        if requesting_command:
            # If the adventure is still running, terminate it
            adventure.send('terminate')

        adventure = run_text_adventure(s)

        block, requesting_command = next(adventure)

        if target_room is not None:
            initial_room = parse_room_block(block)

            # Get back to the target room
            for command in find_command_sequence(rooms, connections,
                                                 initial_room['name'], [],
                                                 target_room, []):
                block, requesting_command = adventure.send(command)

    rooms = {}
    good_items = set()
    trap_items = set()

    connections = collections.defaultdict(dict)

    def explore(room):
        nonlocal block, requesting_command
        if 'items' in room:
            for item in room['items']:
                block, requesting_command = adventure.send('take ' + item)
                if not requesting_command:
                    # Crashed, must be a trap item
                    inv = None
                else:
                    block, requesting_command = adventure.send('inv')
                    try:
                        inv = parse_inventory(block)
                    except AssertionError:
                        # Wasn't inventory output, must be a trap item
                        inv = None

                if inv is None or item not in inv:
                    print(f'"{item}" is a trap item!')
                    trap_items.add(item)
                    restart(room['name'])
                    continue

                # This item seems to be good!
                good_items.add(item)

        if room['name'] == SECURITY:
            # Special handling
            unknown_directions = [direction for direction in room['doors']
                                  if direction not in connections[SECURITY]]
            assert(len(unknown_directions) == 1)

            direction = unknown_directions[0]
            reverse_direction = REVERSE_DIRECTIONS[direction]

            rooms[VALIDATION] = {'name': VALIDATION,
                                 'doors': [reverse_direction]}

            connections[SECURITY][direction] = VALIDATION
            connections[VALIDATION][reverse_direction] = SECURITY

            return

        for direction in room['doors']:
            if direction in connections[room['name']]:
                # We know what's this direction already
                continue

            reverse_direction = REVERSE_DIRECTIONS[direction]

            block, requesting_command = adventure.send(direction)

            next_room = parse_room_block(block)

            rooms[next_room['name']] = next_room

            connections[room['name']][direction] = next_room['name']
            connections[next_room['name']][reverse_direction] = room['name']

            explore(next_room)

            # Backtrack
            block, requesting_command = adventure.send(reverse_direction)

    # Initialize the adventure
    restart(None)

    initial_room = parse_room_block(block)
    rooms[initial_room['name']] = initial_room

    # Explore the ship
    explore(initial_room)

    # What's in our inventory right now?
    block, requesting_command = adventure.send('inv')
    inventory = parse_inventory(block)

    # Pick up any missing items and move to security
    for command in find_command_sequence(rooms, connections,
                                         initial_room['name'], inventory,
                                         SECURITY, good_items):
        block, requesting_command = adventure.send(command)

    # Which way goes to the security validation?
    validation_command = None
    for direction, dest in connections[SECURITY].items():
        if dest == VALIDATION:
            validation_command = direction
    assert(validation_command is not None)

    # Now crack security!
    good_items = sorted(good_items)

    # Currently we have all items in our inventory
    inv_mask = 2 ** len(good_items) - 1

    options = list(range(2 ** len(good_items)))

    # Check options while minimizing inventory switches between trials.
    # This may not be the optimal cracking strategy but it's pretty efficient
    # since each guess will prune the option space and most times only one
    # inventory switch is required between trials.
    while requesting_command:
        # TODO: Maybe row.bit_count() with Python 3.10?
        next_trial = min(options,
                         key=lambda mask: gmpy2.popcount(mask ^ inv_mask))
        swaps = next_trial ^ inv_mask

        mask = 1
        for obj in good_items:
            if swaps & mask:
                if inv_mask & mask:
                    block, requesting_command = adventure.send('drop ' + obj)
                else:
                    block, requesting_command = adventure.send('take ' + obj)
            mask <<= 1
        inv_mask = next_trial

        block, requesting_command = adventure.send(validation_command)

        if requesting_command:
            m = re.search('Droids on this ship are (\w+) than the detected value',
                          block)

            if m.group(1) == 'heavier':
                # This was too light
                # Exclude options which are strict subsets of this pool
                options = [o for o in options
                           if o != (o & inv_mask)]
            else:
                assert(m.group(1) == 'lighter')
                # This was too heavy
                # Exclude options which include every item from this pool
                options = [o for o in options
                           if inv_mask != (o & inv_mask)]

    # Report what we found!
    required_items = []
    mask = 1
    for obj in good_items:
        if inv_mask & mask:
            required_items.append(obj)
        mask <<= 1

    print()
    print(f'Required items for security: {", ".join(required_items)}')

    optimal_sequence = find_command_sequence(rooms, connections,
                                             initial_room['name'], [],
                                             SECURITY, required_items)
    optimal_sequence.append(validation_command)

    print('Optimal command sequence:')
    print('\n'.join(optimal_sequence))

    last_line = block.split('\n')[-1]
    m = re.search('\d+', last_line)

    answer = int(m.group(0))

    print()
    print(last_line)
    return answer

def part1(s):
    answer = solve_text_adventure(s)

    print(f'The answer to part one is {answer}')

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2019, 25)
part1(INPUT)
part2(INPUT)
