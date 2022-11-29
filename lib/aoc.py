import contextlib
import datetime
import dateutil.tz
import jsonplus as json
import os
import pathlib
import re
import requests
import shutil
import subprocess
import time
import webbrowser

# TODO: Compare with https://github.com/wimglenn/advent-of-code-data

_s = requests.Session()

_s.headers.update({
    'User-Agent': 'github.com/morgoth1145/advent-of-code by phogg@novamoon.net'
})

_account_selection = None

def select_account(account=None):
    global _account_selection
    _account_selection = account
    del _s.cookies['session']

def _get_root_cache_directory():
    return pathlib.Path.home() / '.advent-of-code'

def _get_cache_directory():
    p = _get_root_cache_directory()
    if _account_selection is None:
        return p

    return p / _account_selection

# Used to ensure that multiple Python instances don't bypass the rate limits!
@contextlib.contextmanager
def _locked_file(path, mode, timeout=None):
    # Borrows heavily from a file locking mechanism from Stack Overflow
    # https://stackoverflow.com/questions/489861/locking-a-file-in-python/498505#498505
    import errno

    class FileLockException(Exception):
        pass

    printed_long_wait_warning = False
    TIME_UNTIL_LONG_WAIT_WARNING = datetime.timedelta(seconds=15)

    lock_path = path + '.lock'

    start_time = datetime.datetime.now()

    fd = None
    try:
        exists = False
        while fd is None:
            try:
                fd = os.open(lock_path, os.O_CREAT|os.O_EXCL|os.O_RDWR)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

                if not printed_long_wait_warning:
                    now = datetime.datetime.now()
                    waited = now - start_time

                    if waited > TIME_UNTIL_LONG_WAIT_WARNING:
                        try:
                            with open(lock_path, 'r') as lock_f:
                                lock_desc = lock_f.read()
                        except FileNotFoundError:
                            # Maybe the file was unlocked in the interim?
                            continue

                        printed_long_wait_warning = True
                        print(f'Warning: Waiting a long time to lock file {path}...')
                        print(f'Lock file contents: {lock_desc}')

                time.sleep(0.05)

        if printed_long_wait_warning:
            print(f'Finally locked file {path}!')

        with os.fdopen(fd, 'a') as lock_f:
            lock_f.write(f'Locked by Python process {os.getpid()}')
            lock_f.flush()
            with open(path, mode) as f:
                yield f
    finally:
        if fd is not None:
            os.unlink(lock_path)

_RATE_LIMIT_MIN_TIMES = {
    'fetch_input': datetime.timedelta(seconds=5),
    'submit_answer': datetime.timedelta(milliseconds=500), # In practice shouldn't get hit (rate limiting due to bad answers and just solving part 2 will take time) but just in case
    'submit_answer_alt_account': datetime.timedelta(seconds=10), # May be hit in alt account testing/timings
    'get_puzzle_page': datetime.timedelta(seconds=1), # In practice other throttles should delay things
    'verify_login': datetime.timedelta(seconds=1), # In practice shouldn't be issued to often, but rate limit just in case
}

def _rate_limit(action_type):
    if action_type == 'submit_answer' and _account_selection is not None:
        action_type = 'submit_answer_alt_account'

    if action_type not in _RATE_LIMIT_MIN_TIMES:
        print(f'Warning: Rate limiter does not know about {action_type}, will default to 1 second rate limit')

    required_wait_time = _RATE_LIMIT_MIN_TIMES.get(action_type, datetime.timedelta(seconds=1))

    file_path = _get_root_cache_directory() / '.rate-limiting' / action_type

    os.makedirs(file_path.parent, exist_ok=True)

    # Ensure that no other Python process slips through while rate limiting
    with _locked_file(str(file_path), 'a+') as actions_f:
        actions_f.seek(0)
        contents = actions_f.read()

        last_time = None
        if contents:
            last_time = json.loads(contents)

        if last_time is not None:
            time_since = datetime.datetime.now(dateutil.tz.tzutc()) - last_time

            to_wait = required_wait_time - time_since

            if to_wait > datetime.timedelta():
                print(f'Waiting {to_wait} until performing action {action_type}...')
                time.sleep(to_wait.total_seconds())

        now = datetime.datetime.now(dateutil.tz.tzutc())

        # Replace entire file
        actions_f.seek(0)
        actions_f.truncate()
        actions_f.write(json.dumps(now))

def _get_cookie_cache_file():
    return _get_cache_directory() / 'session-cookie.txt'

def _forget_session_cookie():
    _get_cookie_cache_file().unlink()
    del _s.cookies['session']

def _load_session_cookie():
    cookie_cache_file = _get_cookie_cache_file()

    if not cookie_cache_file.exists():
        account_desc = _account_selection
        if account_desc is None:
            account_desc = 'Main'

        cookie_cache_file.write_text(f'''A new Advent of Code session cookie is needed. Please do the following:
1) Log into your {account_desc} account in chrome
2) Open this in chrome: chrome://settings/cookies/detail?site=adventofcode.com
3) Look at the session cookie and copy the value/content
4) Replace this file with that cookie''')

        subprocess.check_call(['notepad', cookie_cache_file])

    _s.cookies['session'] = cookie_cache_file.read_text().rstrip('\n')

def _get_input_cache_file(year, day):
    return _get_cache_directory() / str(year) / f'day-{day}.txt'

def _get_time_trial_file(year, day):
    return _get_cache_directory() / str(year) / f'day-{day}-time-trial.json'

def _get_solution_cache_file(year, day):
    return _get_cache_directory() / str(year) / f'day-{day}-solutions.json'

def _get_puzzle_page(year, day):
    url = f'https://adventofcode.com/{year}/day/{day}'
    _load_session_cookie()

    _rate_limit('get_puzzle_page')

    r = _s.get(url)
    r.raise_for_status()
    return r.text

def _get_puzzle_answers(year, day):
    puzzle = _get_puzzle_page(year, day)
    answers = []
    for a in re.findall('Your puzzle answer was <code>(.*?)</code>', puzzle):
        answers.append(a)
    while len(answers) != 2:
        answers.append(None)
    return answers

def time_to_release(year, day):
    # Puzzles release at midnight EST (UTC-5)
    release_time = datetime.datetime(year=year,
                                     month=12,
                                     day=day,
                                     hour=5,
                                     tzinfo=dateutil.tz.tzutc())
    now = datetime.datetime.now(dateutil.tz.tzutc())
    return release_time - now

def get_input(year, day):
    '''
get_input returns the input for a given problem (by year/day)
It downloads these inputs from the server on-demand, intelligently caching them on disk
to avoid pinging the server repeatedly. It also has rudimentary handling to detect
login issues and premature inputs
    '''
    notLoggedInFile = 'Puzzle inputs differ by user.  Please log in to get your puzzle input.'
    tooEarlyFile = 'Please don\'t repeatedly request this endpoint before it unlocks! The calendar countdown is synchronized with the server time; the link will be enabled on the calendar the instant this puzzle becomes available.'

    input_file_path = _get_input_cache_file(year, day)

    if input_file_path.exists():
        contents = input_file_path.read_text().rstrip('\n')
        if contents != notLoggedInFile and contents != tooEarlyFile:
            # The contents are good! (I think)
            return contents

        input_file_path.unlink()
    os.makedirs(input_file_path.parent, exist_ok=True)

    url = f'https://adventofcode.com/{year}/day/{day}/input'
    _load_session_cookie()

    _rate_limit('fetch_input')

    r = _s.get(url)
    if r.status_code != 400:
        # There isn't a client error so we *should* be logged in?
        r.raise_for_status()
        input_file_path.write_bytes(r.content)

        contents = input_file_path.read_text().rstrip('\n')
        if contents != notLoggedInFile:
            # The contents are good! (I think)
            return contents

    # The session cookie may be invalid?
    input_file_path.unlink(missing_ok=True)
    _forget_session_cookie()
    _load_session_cookie()

    # Last try
    r = _s.get(url)
    r.raise_for_status()
    input_file_path.write_bytes(r.content)

    return input_file_path.read_text().rstrip('\n')

def download_input_when_live(year, day):
    # Download 3 seconds after release
    to_wait = time_to_release(year, day) + datetime.timedelta(seconds=3)
    to_wait_seconds = to_wait.total_seconds()
    if to_wait_seconds > 0:
        print(f'Waiting {to_wait} until downloading input...')
        time.sleep(to_wait_seconds)
    print(f'Downloading input for {year} day {day}...')
    get_input(year, day)

def forget_input(year, day):
    '''forget_input removes the input from the cache (effectively forcing a re-download on the next attempt)'''
    _get_input_cache_file(year, day).unlink()

def clear_input_cache():
    '''clear_input_cache clears the entire input cache (except for the session cookie)'''
    cache_dir = _get_cache_directory()
    cookie_file = _get_cookie_cache_file()

    os.makedirs(cache_dir, exist_ok=True)

    for child in list(cache_dir.iterdir()):
        if child == cookie_file:
            continue
        shutil.rmtree(child)

def _auto_commit(year, day, part, good_answer_line):
    repo_root = pathlib.Path(__file__).parent.parent

    subprocess.check_call(['git', 'stage', '.'],
                          cwd=repo_root)

    title = f'{year} Day {day} Part {part}'
    if day == 25 and part == 1:
        title += ' (There is no Part 2)'
    msg = f'{title}\n\n{good_answer_line}'

    subprocess.check_call(['git', 'commit', '-m', msg],
                          cwd=repo_root)

def _submit_answer_to_web_impl(year, day, part, answer):
    _load_session_cookie()

    # Day 25 Part 2 is allowed to not be rate limited due to being the final star and
    # being immediately "solvable". Every moment counts for the leaderboard!
    if day != 25 or part != 2:
        _rate_limit('submit_answer')

    url = f'https://adventofcode.com/{year}/day/{day}/answer'
    r = _s.post(url, data={'level': part, 'answer': str(answer)})
    r.raise_for_status()

    answer_webpage_file = _get_cache_directory() / str(year) / f'answer-page-{day}-part-{part}.html'
    with open(answer_webpage_file, 'wb+') as f:
        f.write(r.content)

    if day == 25 and part == 2:
        return True, None

    TOO_RECENT_KEY = 'You gave an answer too recently'
    BAD_ANSWER_KEYS = ["That's not the right answer",
                       "You don't seem to be solving the right level"]
    GOOD_ANSWER_KEY = "That's the right answer!"
    for line in r.text.splitlines():
        if GOOD_ANSWER_KEY in line:
            print(line)
            return True, line # Good answer
        if TOO_RECENT_KEY in line:
            print(line)
            assert(False)
        for k in BAD_ANSWER_KEYS:
            if k in line:
                print(line)
                return False, line

    print('Bad request!')
    assert(False)

def _submit_answer(year, day, part, answer):
    answer_file_path = _get_cache_directory() / str(year) / f'answers-day-{day}.json'
    try:
        with open(answer_file_path) as f:
            tried_answers = json.loads(f.read())
    except:
        tried_answers = {'1':{}, '2':{}}

    if str(answer) in tried_answers[str(part)]:
        print(f'You already submitted {answer} for {year} day {day} part {part}!')
        return

    timeout_until = tried_answers.pop('timeout_until', None)

    now = datetime.datetime.now(dateutil.tz.tzutc())

    if timeout_until is not None:
        to_wait = timeout_until - now
        if to_wait > datetime.timedelta():
            print(f'Waiting for timeout due to bad answer. {to_wait} remains...')
            time.sleep(to_wait.total_seconds())

            # Make sure to record when the answer was *actually* submitted!
            now = datetime.datetime.now(dateutil.tz.tzutc())

    # Don't overwrite times during trials
    if str(answer) not in tried_answers[str(part)]:
        tried_answers[str(part)][str(answer)] = now

    trial = None
    trial_path = _get_time_trial_file(year, day)
    if os.path.exists(trial_path):
        with open(trial_path) as f:
            trial = json.loads(f.read())

    if trial is not None and trial['answers'][str(part)] is not None:
        good_answer = (str(answer) == trial['answers'][str(part)])
        answer_line = None
    else:
        good_answer, answer_line = _submit_answer_to_web_impl(year,
                                                              day,
                                                              part,
                                                              answer)

    if not good_answer:
        m = re.search('Please wait (.*) before trying again', answer_line)
        if m is None:
            print('Warning: Cannot detect timeout from answer line. Defaulting to 1 minute.')
            timeout = datetime.timedelta(minutes=1)
        else:
            timeout = {'one minute': datetime.timedelta(minutes=1),
                       '5 minutes': datetime.timedelta(minutes=5)}.get(m.group(1))
            if timeout is None:
                print(f'Warning: Cannot detect timeout from "{m.group(1)}". Defaulting to 1 minute.')
                timeout = datetime.timedelta(minutes=1)
            else:
                print(f'Timeout of {timeout} due to bad answer...')

        timeout_until = datetime.datetime.now(dateutil.tz.tzutc()) + timeout
        tried_answers['timeout_until'] = timeout_until

    with open(answer_file_path, 'w+') as f:
        f.write(json.dumps(tried_answers))

    if good_answer:
        if trial is not None:
            delta = now - trial['begin']
            trial['times'][str(part)] = delta
            with open(trial_path, 'w+') as f:
                f.write(json.dumps(trial))

            answer_line = f'Time: {delta}'
            print(f'It took {delta} to finish {year} Day {day} Part {part}')

        if day == 25 and part == 1:
            # Immediately auto-submit day 25 part 2 for maximum efficiency
            _submit_answer(year, 25, 2, 1)

        if day != 25 or part != 2:
            if _account_selection is None:
                # Auto-commit to save the human time!
                _auto_commit(year, day, part, answer_line)

    return good_answer

def give_answer(year, day, part, answer):
    if isinstance(answer, float):
        print(f'Warning: Provided answer ({answer}) is a float! That is not expected')
        alternate = int(answer)
        if input(f'Use {alternate} instead? ').lower() in ('y', 'yes', '1'):
            answer = alternate

    solution_cache_path = _get_solution_cache_file(year, day)
    if os.path.exists(solution_cache_path):
        with open(solution_cache_path) as f:
            solutions = json.loads(f.read())
    else:
        # TODO: Maybe query the page? (Only if this isn't a live problem!)
        solutions = [None, None]

    target = solutions[part-1]

    if part == 1:
        print(f'The answer to part one is {answer}')
    else:
        assert(part == 2)
        print(f'The answer to part two is {answer}')

    if target is not None:
        if str(answer) != target:
            print('Invalid answer!')
            assert(False)
    else:
        if _account_selection is None:
            if input('Submit answer? ').lower() not in ('y', 'yes', '1'):
                print('Aborting...')
                assert(False)
        else:
            today = datetime.datetime.now(dateutil.tz.tzutc())
            if year == today.year:
                print('Alternate accounts are for stress testing solution code, not running on the current year\'s problems while they are still live! Please wait until January to run on alternate accounts.')
                assert(False)

        assert(_submit_answer(year, day, part, answer))

        # If we get here then the answer must have been good
        solutions[part-1] = str(answer)

        with open(solution_cache_path, 'w+') as f:
            f.write(json.dumps(solutions))

def knows_solutions_for(year, day):
    solution_cache_path = _get_solution_cache_file(year, day)
    if not os.path.exists(solution_cache_path):
        return False

    with open(solution_cache_path) as f:
        solutions = json.loads(f.read())

    return None not in solutions

def open_pages_for(year, day):
    webbrowser.open(f'https://adventofcode.com/{year}/day/{day}')
    webbrowser.open(f'https://adventofcode.com/{year}/day/{day}/input')

def begin_time_trial(year, day):
    trial_path = _get_time_trial_file(year, day)
    if os.path.exists(trial_path):
        print(f'Time trial already started!')
        return

    # Make sure the input is downloaded
    get_input(year, day)

    p1, p2 = _get_puzzle_answers(year, day)

    trial = {
        'begin': datetime.datetime.now(dateutil.tz.tzutc()),
        'answers': {1: p1, 2: p2},
        'times': {1: None, 2: None}
    }

    with open(trial_path, 'w+') as f:
        f.write(json.dumps(trial))

    open_pages_for(year, day)

def ensure_valid_session_cookie():
    '''
ensure_valid_session_cookie checks to see if the current session cookie is valid.
If it is not, it forgets the cookie and asks for a new one.
    '''
    def currently_logged_in():
        r = _s.get('https://adventofcode.com/support')

        # Check the status 4 ways to be paranoid
        logged_out = '[Log In]' in r.text
        logged_out_2 = 'You are not logged in.' in r.text
        logged_in = '[Log Out]' in r.text
        logged_in_2 = 'Because you are logged in,' in r.text

        assert(logged_out == logged_out_2)
        assert(logged_in == (not logged_out))
        assert(logged_in_2 == (not logged_out_2))

        return logged_in

    _rate_limit('verify_login')

    _load_session_cookie()
    if not currently_logged_in():
        _forget_session_cookie()
        _load_session_cookie()
        assert(currently_logged_in())

def cache_solutions(year, day):
    solution_cache_path = _get_solution_cache_file(year, day)
    if os.path.exists(solution_cache_path):
        with open(solution_cache_path) as f:
            solutions = json.loads(f.read())

        if all(s is not None
               for s in solutions):
            # The solutions are already cached
            return

    solutions = _get_puzzle_answers(year, day)

    if all(s is None
           for s in solutions):
        # No known solutions (yet)
        return

    with open(solution_cache_path, 'w+') as f:
        f.write(json.dumps(solutions))
