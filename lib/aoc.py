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

def _get_cache_directory():
    return pathlib.Path.home() / '.advent-of-code'

def _read_file_as_string(path):
    with open(path) as f:
        return f.read().rstrip('\n')

def _get_cookie_cache_file():
    return _get_cache_directory() / 'session-cookie.txt'

def _forget_session_cookie():
    _get_cookie_cache_file().unlink()
    del _s.cookies['session']

def _load_session_cookie():
    cookie_cache_file = _get_cookie_cache_file()

    if not cookie_cache_file.exists():
        cookie_cache_file.write_text('''A new Advent of Code session cookie is needed. Please do the following:
1) Open this in chrome: chrome://settings/cookies/detail?site=adventofcode.com
2) Look at the session cookie and copy the value/content
3) Replace this file with that cookie''')

        subprocess.check_call(['notepad', cookie_cache_file])

    _s.cookies['session'] = cookie_cache_file.read_text().rstrip('\n')

def _download_file(url, file_path):
    r = _s.get(url)
    r.raise_for_status()
    file_path.write_bytes(r.content)

def _get_input_cache_file(year, day):
    return _get_cache_directory() / str(year) / f'day-{day}.txt'

def _get_time_trial_file(year, day):
    return _get_cache_directory() / str(year) / f'day-{day}-time-trial.json'

def _get_puzzle_page(year, day):
    url = f'https://adventofcode.com/{year}/day/{day}'
    _load_session_cookie()

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

    _download_file(url, input_file_path)

    contents = input_file_path.read_text().rstrip('\n')
    if contents != notLoggedInFile:
        # The contents are good! (I think)
        return contents

    # The session cookie may be invalid?
    input_file_path.unlink()
    _forget_session_cookie()
    _load_session_cookie()

    # Last try
    _download_file(url, input_file_path)
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

def auto_commit(year, day, part, good_answer_line):
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
                return False, None

    print('Bad request!')
    assert(False)

def submit_answer(year, day, part, answer):
    answer_file_path = _get_cache_directory() / str(year) / f'answers-day-{day}.json'
    try:
        with open(answer_file_path) as f:
            tried_answers = json.loads(f.read())
    except:
        tried_answers = {'1':{}, '2':{}}

    if str(answer) in tried_answers[str(part)]:
        print(f'You already submitted {answer} for {year} day {day} part {part}!')
        return

    now = datetime.datetime.now(dateutil.tz.tzutc())

    tried_answers[str(part)][str(answer)] = now

    trial = None
    trial_path = _get_time_trial_file(year, day)
    if os.path.exists(trial_path):
        with open(trial_path) as f:
            trial = json.loads(f.read())

    if trial is not None and trial['answers'][str(part)] is not None:
        good_answer = (str(answer) == trial['answers'][str(part)])
        good_answer_line = None
    else:
        good_answer, good_answer_line = _submit_answer_to_web_impl(year,
                                                                   day,
                                                                   part,
                                                                   answer)

    with open(answer_file_path, 'w+') as f:
        f.write(json.dumps(tried_answers))

    if good_answer:
        if trial is not None:
            delta = now - trial['begin']
            trial['times'][str(part)] = delta
            with open(trial_path, 'w+') as f:
                f.write(json.dumps(trial))

            print(f'It took {delta} to finish {year} Day {day} Part {part}')

        if day == 25 and part == 1:
            # Immediately auto-submit day 25 part 2 for maximum efficiency
            submit_answer(year, 25, 2, 1)

        if day != 25 or part != 2:
            # Auto-commit to save the human time!
            auto_commit(year, day, part, good_answer_line)

    return good_answer

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

    # Open the web pages
    webbrowser.open(f'https://adventofcode.com/{year}/day/{day}')
    webbrowser.open(f'https://adventofcode.com/{year}/day/{day}/input')
