'''
authentication.py
'''
import flask

from serverlib import logger
from serverlib import database



def check_token(function):
    '''
    token(function)
    '''
    def wrapper(*args, **kwargs):
        user_id = int(flask.request.headers['LOM_id'])
        token = flask.request.headers['LOM_token']
        response = database.check_token(user_id, token)
        if response['success']:
            logger.log('check_token', logger.STATUS_SUCCESS, f"id: {user_id}")
            new_token = response['token']
            response = function(*args, **kwargs)
            response['token'] = new_token
            return response
        logger.log('check_token', logger.STATUS_ERROR, str(response['error']))
        return {
            'success': False,
            'error': response['error']
        }
    wrapper.__name__ = function.__name__
    return wrapper
