'''
loggerconsole.py
'''
import datetime

from serverlib import commons



_config = commons.config['loggerconsole']



_COLOR_NONE = '\033[0m'
_COLOR_BLUE = '\033[94m'
_COLOR_GREEN = '\033[92m'
_COLOR_YELLOW = '\033[93m'
_COLOR_ORANGE = '\033[33m'
_COLOR_RED = '\033[91m'
_COLOR_PURPLE = '\033[95m'

def blue(text):
    '''
    blue(text)
    '''
    return f"{_COLOR_BLUE}{text}{_COLOR_NONE}"

def green(text):
    '''
    green(text)
    '''
    return f"{_COLOR_GREEN}{text}{_COLOR_NONE}"

def yellow(text):
    '''
    yellow(text)
    '''
    return f"{_COLOR_YELLOW}{text}{_COLOR_NONE}"

def orange(text):
    '''
    yellow(text)
    '''
    return f"{_COLOR_ORANGE}{text}{_COLOR_NONE}"

def red(text):
    '''
    red(text)
    '''
    return f"{_COLOR_RED}{text}{_COLOR_NONE}"

def purple(text):
    '''
    purple(text)
    '''
    return f"{_COLOR_PURPLE}{text}{_COLOR_NONE}"

def _log(text):
    '''
    __log(text)
    '''
    print(f"{blue(f'[{datetime.datetime.now()}]')} {text}")

def debug(text):
    '''
    debug(text)
    '''
    if _config['debug']:
        _log(f"{purple('(DEBUG)')} {text}")

def query(text):
    '''
    query(text)
    '''
    if _config['query']:
        _log(f"{orange('(QUERY)')} {text}")

def api(text):
    '''
    api(text)
    '''
    if _config['api']:
        _log(f"{green('(API)')} {text}")

def info(text):
    '''
    info(text)
    '''
    if _config['info']:
        _log(f"(INFO) {text}")

def error(text):
    '''
    error(text)
    '''
    if _config['error']:
        _log(red(f"(ERROR) {text}"))
