'''
login.py
'''
import json
import secrets
import flask

from serverlib import database



router = flask.Blueprint('login', __name__)



@router.route('', methods=['GET'])
def get_login():
    '''
    get_login()
    '''
    return flask.send_file('static/html/login.html')



@router.route('', methods=['POST'])
def post_login():
    '''
    post_login()
    '''
    data_dict = json.loads(flask.request.data.decode())
    response = database.check_active(data_dict['username'])
    if response['success']:
        response = database.check_password(data_dict['username'], data_dict['password'])
        if response['success']:
            user_id = response['id']
            token = secrets.token_hex()
            response = database.create_session(user_id, token)
            if response['success']:
                return {
                    'success': True,
                    'id': user_id,
                    'token': token
                }
            return {
                'success': False,
                'error': response['error']
            }
        return {
            'success': False,
            'error': response['error']
        }
    return {
        'success': False,
        'error': response['error']
    }
