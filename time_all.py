import collections
import sys
import time

import lib.aoc

SHORTEST_TIMES_TO_REPORT = 5
LONGEST_TIMES_TO_REPORT = 15

ACCOUNTS_TO_TEST = [
    None,
    'github',
    'google',
    'twitter',
    'reddit',
]

YEARS_TO_TEST = range(2015, 2023)
DAYS_TO_TEST = range(1, 26)

for account in ACCOUNTS_TO_TEST:
    lib.aoc.select_account(account)
    lib.aoc.ensure_valid_session_cookie()

timings = collections.defaultdict(dict)

for account in ACCOUNTS_TO_TEST:
    lib.aoc.select_account(account)
    for year in YEARS_TO_TEST:
        for day in DAYS_TO_TEST:
            print(f'{account} {year} day {day}:')

            # Prefetch the input to make sure that the timing is accurate
            lib.aoc.get_input(year, day)

            # Make sure that any solutions are cached
            lib.aoc.cache_solutions(year, day)

            mod_name = f'{year}.{day:02}.solution'

            start = time.perf_counter()
            m = __import__(mod_name)
            end = time.perf_counter()

            # Unload the module so that it is reloaded in the next iteration
            del sys.modules[mod_name]

            timings[f'{year}.{day}'][account] = end - start

total_times = sorted((sum(account_times.values()), day_key)
                     for day_key, account_times in timings.items())

full_runtime = sum(t for t, key in total_times)

SHORTEST_TIMES_TO_REPORT = 5
LONGEST_TIMES_TO_REPORT = 15

def print_days(day_total_times):
    rows = []

    for total_time, day_key in day_total_times:
        min_time = min(timings[day_key].values())
        average_time = total_time / len(ACCOUNTS_TO_TEST)
        max_time = max(timings[day_key].values())

        day_key = f'{day_key:<7}' # Should be left justified unlike the rest
        total_time = f'{total_time*1000:.1f} ms'
        average_time = f'{average_time*1000:.1f} ms'
        min_time = f'{min_time*1000:.1f} ms'
        max_time = f'{max_time*1000:.1f} ms'

        rows.append((day_key, total_time, average_time, min_time, max_time))

    column_widths = [max(len(row[i]) for row in rows)
                     for i
                     in range(len(rows[0]))]

    for row in rows:
        row = (' ' * (width - len(item)) + item
               for item, width
               in zip(row, column_widths))

        day_key, total_time, average_time, min_time, max_time = row

        print(f'{day_key} took {total_time} total, min: {min_time}, average: {average_time}, max: {max_time}')

print('-'*75)
print(f'{SHORTEST_TIMES_TO_REPORT} shortest days to run:')
print_days(total_times[:SHORTEST_TIMES_TO_REPORT])
print(f'{LONGEST_TIMES_TO_REPORT} longest days to run:')
print_days(total_times[-LONGEST_TIMES_TO_REPORT:])
print(f'Total time for all days: {full_runtime} seconds')
