'''
logger.py
'''
import json

from serverlib import loggerconsole
from serverlib import loggerdatabase



with open('config.json', 'r', encoding='utf-8') as f:
    __config = json.loads(f.read())['logger']
    f.close()



STATUS_SUCCESS = 'success'
STATUS_ERROR = 'error'



def log(operation, status, log):
    '''
    log(operation, status, log)
    '''
    if __config['log']:
        if status == STATUS_SUCCESS:
            loggerconsole.info(f"({operation}) {log}")
        elif status == STATUS_ERROR:
            loggerconsole.error(f"({operation}) {log}")
        loggerdatabase.create_log(operation, status, log)
