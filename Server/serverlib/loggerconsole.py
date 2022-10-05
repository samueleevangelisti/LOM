'''
loggerconsole.py
'''
import json
import datetime



with open('config.json', 'r', encoding='utf-8') as f:
    __config = json.loads(f.read())['loggerconsole']
    f.close()



__COLOR_NONE = '\033[0m'
__COLOR_BLUE = '\033[94m'
__COLOR_GREEN = '\033[92m'
__COLOR_YELLOW = '\033[93m'
__COLOR_ORANGE = '\033[33m'
__COLOR_RED = '\033[91m'
__COLOR_PURPLE = '\033[95m'

def blue(text):
    '''
    blue(text)
    '''
    return f"{__COLOR_BLUE}{text}{__COLOR_NONE}"

def green(text):
    '''
    green(text)
    '''
    return f"{__COLOR_GREEN}{text}{__COLOR_NONE}"

def yellow(text):
    '''
    yellow(text)
    '''
    return f"{__COLOR_YELLOW}{text}{__COLOR_NONE}"

def orange(text):
    '''
    yellow(text)
    '''
    return f"{__COLOR_ORANGE}{text}{__COLOR_NONE}"

def red(text):
    '''
    red(text)
    '''
    return f"{__COLOR_RED}{text}{__COLOR_NONE}"

def purple(text):
    '''
    purple(text)
    '''
    return f"{__COLOR_PURPLE}{text}{__COLOR_NONE}"

def __log(text):
    '''
    __log(text)
    '''
    print(f"{blue(f'[{datetime.datetime.now()}]')} {text}")

def debug(text):
    '''
    debug(text)
    '''
    if __config['debug']:
        __log(f"{purple('(DEBUG)')} {text}")

def query(text):
    '''
    query(text)
    '''
    if __config['query']:
        __log(f"{orange('(QUERY)')} {text}")

def api(text):
    '''
    api(text)
    '''
    if __config['api']:
        __log(f"(API) {text}")

def info(text):
    '''
    info(text)
    '''
    if __config['info']:
        __log(f"(INFO) {text}")

def error(text):
    '''
    error(text)
    '''
    if __config['error']:
        __log(red(f"(ERROR) {text}"))
