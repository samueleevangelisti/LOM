import json

from .database_core import DatabaseLog



f = open('config.json', 'r')
config = json.loads(f.read())['logger']
f.close()



class Logger:
    __config = config
    state_success = 'success'
    state_error = 'error'

    def debug(text):
        if Logger.__config['debug']:
            print(text)

    def log(operation, state, log):
        if Logger.__config['log']:
            DatabaseLog.create_log(operation, state, str(log))
