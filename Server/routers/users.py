'''
users.py
'''
import json
import random
import flask

from serverlib import commons
from serverlib import utils
from serverlib import database



_config = commons.config['server']



router = flask.Blueprint('users', __name__)



@router.route('', methods=['GET'])
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



@router.route('', methods=['POST'])
def post_user():
    '''
    post_user()
    '''
    response = database.retrieve_users()
    if len(response) < 10 ** _config['pin_length']:
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
                pin = commons.get_pin()
                response = database.update_pin(patch_user_id, pin)
                if not response['success']:
                    return {
                        'success': False,
                        'error': response['error']
                    }
                response_dict['pin'] = pin
            else:
                pin = database.retrieve_users({
                    'id': patch_user_id
                })
                response = database.delete_pin(patch_user_id)
                if not response['success']:
                    return {
                        'success': False,
                        'error': response['error']
                    }
                commons.put_pin(pin)
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
