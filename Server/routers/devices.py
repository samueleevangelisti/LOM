'''
devices.py
'''
import json
import flask

from serverlib import database, utils
from drivers import drivermap


router = flask.Blueprint('devices', __name__)



@router.route('/', methods=['GET'])
@utils.check_token
def get_devices():
    '''
    get_devices()
    '''
    return {
        'success': True,
        'data': database.retrieve_all_devices()
    }



@router.route('/<string:driver>/<string:method>', methods=['POST'])
def post_device_method(driver, method):
    '''
    post_device_method
    '''
    data_dict = json.loads(flask.request.data.decode())
    return drivermap.driver_map[driver][method](data_dict)



@router.route('/', methods=['POST'])
@utils.check_token
def post_device():
    '''
    post_device()
    '''
    user_id = int(flask.request.headers['LOM_id'])
    response = database.check_level(user_id, database.USER_LEVEL_ADMIN)
    if response['success']:
        data_dict = json.loads(flask.request.data.decode())
        response = database.create_device(data_dict['name'], data_dict['url'], data_dict['body'])
        if response['success']:
            return {
                'success': True
            }
        return {
            'success': False,
            'error': response['error']
        }
    return {
        'success': False,
        'error': response['error']
    }



@router.route('/<int:delete_device_id>', methods=['DELETE'])
@utils.check_token
def delete_device(delete_device_id):
    '''
    delete_device()
    '''
    user_id = int(flask.request.headers['LOM_id'])
    response = database.check_level(user_id, database.USER_LEVEL_ADMIN)
    if response['success']:
        response = database.delete_device(delete_device_id)
        if response['success']:
            return {
                'success': True
            }
        return {
            'success': False,
            'error': response['error']
        }
    return {
        'success': False,
        'error': response['error']
    }
