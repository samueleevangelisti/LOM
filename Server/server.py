import flask
from flask import send_file, send_from_directory
import json
import secrets
import random

from server_lib.database import Database



f = open('config.json', 'r')
config = json.loads(f.read())['server']
f.close()



api = flask.Flask(__name__)



@api.route('/', methods=['GET'])
@api.route('/index', methods=['GET'])
@api.route('/index.html', methods=['GET'])
def get_index():
    return send_file('static/html/login.html')



@api.route('/assets/<path:path>', methods=['GET'])
def get_asset(path):
    return send_from_directory('static', path)



@api.route('/login', methods=['POST'])
def post_login():
    data_dict = json.loads(flask.request.data.decode())
    response = Database.check_password(data_dict['username'], data_dict['password'])
    if response['success']:
        user_id = response['id']
        token = secrets.token_hex()
        response = Database.create_session(user_id, token)
        if response['success']:
            return {
                'success': True,
                'id': user_id,
                'token': token
            }
        else:
            return {
                'success': False,
                'error': response['error']
            }
    else:
        return {
            'success': False,
            'error': response['error']
        }



@api.route('/dashboard', methods=['GET'])
def get_dashboard():
    return send_file('static/html/dashboard.html')



@api.route('/dashboard/sections', methods=['GET'])
def get_dashboard_data():
    user_id = int(flask.request.headers['LOM_id'])
    token = flask.request.headers['LOM_token']
    response = Database.check_token(user_id, token)
    if response['success']:
        new_token = response['token']
        return {
            'success': True,
            'token': new_token,
            'data': {
                'is_devices': True,
                'is_users': Database.check_level(user_id, Database.user_level_admin)['success']
            }
        }
    else:
        return {
            'success': False,
            'error': response['error']
        }



@api.route('/dashboard/devices', methods=['GET'])
def get_devices():
    user_id = int(flask.request.headers['LOM_id'])
    token = flask.request.headers['LOM_token']
    response = Database.check_token(user_id, token)
    if response['success']:
        new_token = response['token']
        return {
            'success': True,
            'token': new_token,
            'data': Database.retrieve_all_devices()
        }
    else:
        return {
            'success': False,
            'error': response['error']
        }



@api.route('/dashboard/users', methods=['GET'])
def get_users():
    user_id = int(flask.request.headers['LOM_id'])
    token = flask.request.headers['LOM_token']
    response = Database.check_token(user_id, token)
    if response['success']:
        new_token = response['token']
        response = Database.check_level(user_id, Database.user_level_admin)
        if response['success']:
            return {
                'success': True,
                'token': new_token,
                'data': Database.retrieve_all_users()
            }
        else:
            return {
                'success': False,
                'token': new_token,
                'error': response['error']
            }
    else:
        return {
            'success': False,
            'error': response['error']
        }



@api.route('/dashboard/users/<int:patch_user_id>', methods=['PATCH'])
def put_user(patch_user_id):
    user_id = int(flask.request.headers['LOM_id'])
    token = flask.request.headers['LOM_token']
    response = Database.check_token(user_id, token)
    if response['success']:
        new_token = response['token']
        response = Database.check_level(user_id, Database.user_level_admin)
        if response['success']:
            data_dict = json.loads(flask.request.data.decode())
            response_dict = {}
            if 'pin' in data_dict:
                if len(data_dict['pin']) > 0:
                    response['success'] = False
                    while not response['success']:
                        pin = ''.join([str(e(None)) for e in [lambda x: random.randint(0, 9)] * config['pin_length']])
                        response = Database.update_pin(user_id, pin)
                    response_dict['pin'] = pin
                if len(data_dict['pin']) == 0:
                    response = Database.delete_pin(user_id)
                    if not response['success']:
                        return {
                            'success': False,
                            'token': new_token,
                            'error': response['error']
                        }
            if 'rfid' in data_dict:
                if len(data_dict['rfid']) == 0:
                    response = Database.delete_rfid(user_id)
                    if not response['success']:
                        return {
                            'success': False,
                            'token': new_token,
                            'error': response['error']
                        }
            return {
                'success': True,
                'token': new_token,
                'data': response_dict
            }
        else:
            return {
                'success': False,
                'token': new_token,
                'error': response['error']
            }
    else:
        return {
            'success': False,
            'error': response['error']
        }



@api.route('/dashboard/users/<int:delete_user_id>', methods=['DELETE'])
def delete_user(delete_user_id):
    user_id = int(flask.request.headers['LOM_id'])
    token = flask.request.headers['LOM_token']
    response = Database.check_token(user_id, token)
    if response['success']:
        new_token = response['token']
        response = Database.check_level(user_id, Database.user_level_admin)
        if response['success']:
            response = Database.check_user_level(user_id, delete_user_id)
            if response['success']:
                response = Database.delete_user(delete_user_id)
                if response['success']:
                    return {
                        'success': True,
                        'token': new_token
                    }
                else:
                    return {
                        'success': True,
                        'token': new_token,
                        'error': respose['error']
                    }
            else:
                return {
                    'success': False,
                    'token': new_token,
                    'error': response['error']
                }
        else:
            return {
                'success': False,
                'token': new_token,
                'error': response['error']
            }
    else:
        return {
            'success': False,
            'error': response['error']
        }



if __name__ == '__main__':
        api.run(port=8080)
