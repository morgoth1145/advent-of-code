import json
import pathlib

from lib.special_characters import FULL_BLOCK

_DATA_FILE_PATH = pathlib.Path(__file__).parent.parent / 'data' / 'letters.json'

def _do_print(coords, x_domain, y_domain):
    print('\n'.join(''.join(FULL_BLOCK if (x,y) in coords else ' '
                            for x in x_domain)
                    for y in y_domain))

def _isolate_chars(coords, x_domain, y_domain):
    last_x = x_domain[0]-1
    for test_x in x_domain:
        if all((test_x,y) not in coords
               for y in y_domain):
            char_x_domain = range(last_x+1, test_x)
            char_coords = {(x,y)
                           for x,y in coords
                           if x in char_x_domain}
            if char_coords:
                yield char_coords, char_x_domain
            last_x = test_x

    char_x_domain = range(last_x+1, x_domain[-1]+1)
    char_coords = {(x,y)
                   for x,y in coords
                   if x in char_x_domain}
    if char_coords:
        yield char_coords, char_x_domain

def parse_coord_set(coords):
    with open(_DATA_FILE_PATH) as f:
        known = json.load(f)
    made_updates = False

    min_x, max_x = None, None
    min_y, max_y = None, None

    for x, y in coords:
        if min_x is None:
            min_x, max_x = x, x
            min_y, max_y = y, y
        else:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

    x_domain = range(min_x, max_x+1)
    y_domain = range(min_y, max_y+1)

    height = len(y_domain)

    showed_full_image = False

    output = ''
    for char_coords, char_x_domain in _isolate_chars(coords, x_domain, y_domain):
        width = len(char_x_domain)
        dimensions = f'{width}x{height}'

        pattern = 0
        mask = 1
        for y in y_domain:
            for x in char_x_domain:
                if (x, y) in char_coords:
                    pattern += mask
                mask <<= 1

        # Use hex strings
        # Big integers don't convert to/from json cleanly!
        pattern = f'{pattern:02x}'

        if dimensions not in known:
            known[dimensions] = {}
        options = known[dimensions]
        char = options.get(pattern)
        if char is None:
            if not showed_full_image:
                showed_full_image = True
                print('Unknown character detected. Trying to parse this output:')
                _do_print(coords, x_domain, y_domain)
                print('If this looks invalid, verify the incoming data')

            print('Unknown character:')
            _do_print(char_coords, char_x_domain, y_domain)
            char = input('What is this character? ')
            assert(len(char) == 1)
            options[pattern] = char
            made_updates = True

        output += char

    print('Parsed text from')
    _do_print(coords, x_domain, y_domain)

    if made_updates:
        with open(_DATA_FILE_PATH, 'w+') as f:
            json.dump(known, f, sort_keys=True)

    return output

def parse_dict(d, include_value):
    return parse_coord_set([c for c, val in d.items()
                            if val == include_value])
