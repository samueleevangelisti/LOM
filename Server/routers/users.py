'''
users.py
'''
import json
import random
import flask

from serverlib import database, utils



with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())['server']
    f.close()



router = flask.Blueprint('users', __name__)



@router.route('/', methods=['GET'])
@utils.check_token
def get_users():
    '''
    get_users()
    '''
    user_id = int(flask.request.headers['LOM_id'])
    response = database.check_level(user_id, database.USER_LEVEL_ADMIN)
    if response['success']:
        return {
            'success': True,
            'data': database.retrieve_users()
        }
    return {
        'success': False,
        'error': response['error']
    }



@router.route('/', methods=['POST'])
def post_user():
    '''
    post_user()
    '''
    response = database.retrieve_users()
    if len(response) < 10 ** config['pin_length']:
        data_dict = json.loads(flask.request.data.decode())
        response = database.create_user(data_dict['username'], data_dict['password'], database.USER_LEVEL_USER, False)
        if response['success']:
            return {
                'success': True
            }
        return {
            'sucess': False,
            'error': response['error']
        }
    return {
        'success': False,
        'error': 'User list full'
    }



@router.route('/<int:patch_user_id>', methods=['PATCH'])
@utils.check_token
def patch_user(patch_user_id):
    '''
    put_user(patch_user_id)
    '''
    user_id = int(flask.request.headers['LOM_id'])
    response = database.check_level(user_id, database.USER_LEVEL_ADMIN, patch_user_id, database.USER_LEVEL_ADMIN)
    if response['success']:
        data_dict = json.loads(flask.request.data.decode())
        response_dict = {}
        if 'pin' in data_dict:
            if data_dict['pin'] is not None:
                response['success'] = False
                while not response['success']:
                    pin = ''.join([str(e(None)) for e in [lambda x: random.randint(0, 9)] * config['pin_length']])
                    response = database.update_pin(patch_user_id, pin)
                response_dict['pin'] = pin
            else:
                response = database.delete_pin(patch_user_id)
                if not response['success']:
                    return {
                        'success': False,
                        'error': response['error']
                    }
        if 'rfid' in data_dict:
            if data_dict['rfid'] is None:
                response = database.delete_rfid(patch_user_id)
                if not response['success']:
                    return {
                        'success': False,
                        'error': response['error']
                    }
                response_dict['rfid'] = data_dict['rfid']
        if 'active' in data_dict:
            response = database.update_active(patch_user_id, data_dict['active'])
            if not response['success']:
                return {
                    'success': False,
                    'error': response['error']
                }
            response_dict['active'] = data_dict['active']
        return {
            'success': True,
            'data': response_dict
        }
    return {
        'success': False,
        'error': response['error']
    }



@router.route('/<int:delete_user_id>', methods=['DELETE'])
@utils.check_token
def delete_user(delete_user_id):
    '''
    delete_user(delete_user_id)
    '''
    user_id = int(flask.request.headers['LOM_id'])
    response = database.check_level(user_id, database.USER_LEVEL_ADMIN, delete_user_id, database.USER_LEVEL_ADMIN)
    if response['success']:
        response = database.delete_user(delete_user_id)
        if response['success']:
            return {
                'success': True,
            }
        return {
            'success': True,
            'error': response['error']
        }
    return {
        'success': False,
        'error': response['error']
    }
