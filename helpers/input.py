import os
import pathlib
import requests
import shutil
import subprocess

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
    file_path.write_bytes(r.content)

def _get_input_cache_file(year, day):
    return _get_cache_directory() / str(year) / f'day-{day}.txt'

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
