'''
esp32.py
'''
from serverlib import database



def action_pin(data_dict):
    '''
    action_pin(data_dict)
    '''
    response = database.check_pin(data_dict['pin'])
    if response['success']:
        return {
            'success': True
        }
    return {
        'success': False,
        'error': response['error']
    }



def action_rfid(data_dict):
    '''
    action_rfid(rfid)
    '''
    response =  database.check_rfid(data_dict['rfid'])
    if response['success']:
        return {
            'success': True
        }
    return {
        'success': False,
        'error': response['error']
    }



def add_rfid(data_dict):
    '''
    add_rfid(data_dict)
    '''
    response = database.check_pin(data_dict['pin'])
    if response['success']:
        response = database.update_rfid(response['id'], data_dict['rfid'])
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


def delete_rfid(data_dict):
    '''
    delete_rfid(data_dict)
    '''
    response = database.check_pin(data_dict['pin'])
    if response['success']:
        response = database.delete_rfid(response['id'])
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



method_map = {
    'action_pin': action_pin,
    'action_rfid': action_rfid,
    'add_rfid': add_rfid,
    'delete_rfid': delete_rfid
}
