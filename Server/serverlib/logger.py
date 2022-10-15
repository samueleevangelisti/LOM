'''
logger.py
'''
from serverlib import commons
from serverlib import loggerconsole
from serverlib import loggerdatabase



_config = commons.config['logger']



STATUS_SUCCESS = 'success'
STATUS_ERROR = 'error'



def log(operation, status, log):
    '''
    log(operation, status, log)
    '''
    if _config['log']:
        if status == STATUS_SUCCESS:
            loggerconsole.info(f"({operation}) {log}")
        elif status == STATUS_ERROR:
            loggerconsole.error(f"({operation}) {log}")
        loggerdatabase.create_log(operation, status, log)
