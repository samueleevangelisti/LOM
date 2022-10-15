'''
database.py
'''
import datetime
import secrets
import bcrypt
import mariadb

from serverlib import commons
from serverlib import logger
from serverlib.databaseconnection import DatabaseConnection



_config = commons.config['database']



_database_connection = DatabaseConnection(_config['database_connection'])
USER_LEVEL_ADMIN = 0
USER_LEVEL_USER = 9

################################################################################

def retrieve_devices(where_dict=None):
    '''
    retrieve_devices(where_dict=None)
    '''
    query_list = []
    arg_tuple = ()
    if where_dict:
        for key in where_dict:
            query_list.append(f"{key} = ?")
            arg_tuple = (*arg_tuple, where_dict[key])
    return _database_connection.query(f"SELECT * FROM Devices{' WHERE ' if len(query_list) > 0 else ''}{', '.join(query_list)};", arg_tuple)

def create_device(name, url):
    '''
    create_device()
    '''
    try:
        _database_connection.query('INSERT INTO Devices(name, url) VALUES (?, ?);', (name, url, ))
        logger.log('create_device', logger.STATUS_SUCCESS, f"name: {name}")
        return {
            'success': True
        }
    except mariadb.Error as error:
        logger.log('create_device', logger.STATUS_ERROR, str(error))
        return {
            'success': False,
            'error': str(error)
        }

def delete_device(device_id):
    '''
    delete_device(device_id)
    '''
    try:
        _database_connection.query('DELETE FROM Devices WHERE id = ?;', (device_id, ))
        logger.log('delete_device', logger.STATUS_SUCCESS, f"id: {device_id}")
        return {
            'success': True
        }
    except mariadb.Error as error:
        logger.log('delete_device', logger.STATUS_ERROR, str(error))
        return {
            'success': False,
            'error': str(error)
        }

################################################################################

def retrieve_users(where_dict=None):
    '''
    retrieve_users(where_dict=None)
    '''
    query_list = []
    arg_tuple = ()
    if where_dict:
        for key in where_dict:
            query_list.append(f"{key} = ?")
            arg_tuple = (*arg_tuple, where_dict[key])
    row_list = _database_connection.query(f"SELECT * FROM Users{' WHERE ' if len(query_list) > 0 else ''}{', '.join(query_list)};", arg_tuple)
    for row in row_list:
        row['active'] = bool(row['active'])
        row.pop('password')
    return row_list

def create_user(username, password, level, active):
    '''
    create_user(username, password, level, active)
    '''
    if len(_database_connection.query('SELECT * FROM Users WHERE username = ?;', (username, ))) == 0:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            _database_connection.query('INSERT INTO Users(username, password, level, active) VALUES (?, ?, ?, ?);', (username, password_hash, level, active, ))
            logger.log('create_user', logger.STATUS_SUCCESS, f"username: {username}")
            return {
                'success': True
            }
        except mariadb.Error as error:
            logger.log('create_user', logger.STATUS_ERROR, str(error))
            return {
                'success': False,
                'error': str(error)
            }
    error = f"Username `{username}` already exists"
    logger.log('create_user', logger.STATUS_ERROR, error)
    return {
        'success': False,
        'error': error
    }

def delete_user(user_id):
    '''
    delete_user(user_id)
    '''
    try:
        _database_connection.query('DELETE FROM Users WHERE id = ?;', (user_id, ))
        logger.log('delete_user', logger.STATUS_SUCCESS, f"id: {user_id}")
        return {
            'success': True
        }
    except mariadb.Error as error:
        logger.log('delete_user', logger.STATUS_ERROR, str(error))
        return {
            'success': False,
            'error': str(error)
        }

def update_pin(user_id, pin):
    '''
    update_pin(user_id, pin)
    '''
    try:
        _database_connection.query('UPDATE Users SET pin = ? WHERE id = ?;', (pin, user_id, ))
        logger.log('update_pin', logger.STATUS_SUCCESS, f"id: {user_id}")
        return {
            'success': True
        }
    except mariadb.Error as error:
        logger.log('update_pin', logger.STATUS_ERROR, str(error))
        return {
            'success': False,
            'error': str(error)
        }

def delete_pin(user_id):
    '''
    delete_pin(user_id)
    '''
    try:
        _database_connection.query('UPDATE Users SET pin = NULL WHERE id = ?;', (user_id, ))
        logger.log('delete_pin', logger.STATUS_SUCCESS, f"id: {user_id}")
        return {
            'success': True
        }
    except mariadb.Error as error:
        logger.log('delete_pin', logger.STATUS_ERROR, str(error))
        return {
            'success': False,
            'error': str(error)
        }

def update_rfid(user_id, rfid):
    '''
    update_rfid(user_id, rfid)
    '''
    try:
        _database_connection.query('UPDATE Users SET rfid = ? WHERE id = ?;', (rfid, user_id, ))
        logger.log('update_rfid', logger.STATUS_SUCCESS, f"id: {user_id}")
        return {
            'success': True
        }
    except mariadb.Error as error:
        logger.log('update_rfid', logger.STATUS_ERROR, str(error))
        return {
            'success': False,
            'error': str(error)
        }

def delete_rfid(user_id):
    '''
    delete_rfid(user_id)
    '''
    try:
        _database_connection.query('UPDATE Users SET rfid = NULL WHERE id = ?;', (user_id, ))
        logger.log('delete_rfid', logger.STATUS_SUCCESS, f"id: {user_id}")
        return {
            'success': True
        }
    except mariadb.Error as error:
        logger.log('delete_pin', logger.STATUS_ERROR, str(error))
        return {
            'success': False,
            'error': str(error)
        }

def update_active(user_id, active):
    '''
    update_active(user_id, active)
    '''
    try:
        _database_connection.query('UPDATE Users SET active = ? WHERE id = ?;', (active, user_id, ))
        logger.log('update_active', logger.STATUS_SUCCESS, f"id: {user_id}")
        return {
            'success': True
        }
    except mariadb.Error as error:
        logger.log('update_active', logger.STATUS_ERROR, str(error))
        return {
            'success': False,
            'error': str(error)
        }

def check_password(username, password):
    '''
    check_password(username, password)
    '''
    row_list = _database_connection.query('SELECT id, password FROM Users WHERE username = ?;', (username, ))
    if len(row_list) > 0:
        user_id = row_list[0]['id']
        password_hash = row_list[0]['password']
        if bcrypt.checkpw(password.encode(), password_hash.encode()):
            logger.log('check_password', logger.STATUS_SUCCESS, f"username: {username}")
            return {
                'success': True,
                'id': user_id
            }
        error = f"Invalid password for username `{username}`"
        logger.log('check_password', logger.STATUS_ERROR, error)
        return {
            'success': False,
            'error': error
        }
    error = f"Username `{username}` not registered"
    logger.log('check_password', logger.STATUS_ERROR, error)
    return {
        'success': False,
        'error': error
    }

def check_pin(pin):
    '''
    check_pin(pin)
    '''
    row_list = retrieve_users({
        'pin': pin
    })
    if len(row_list) > 0:
        user_id = row_list[0]['id']
        logger.log('check_pin', logger.STATUS_SUCCESS, f"id: {user_id}")
        return {
            'success': True,
            'id': user_id
        }
    error = f"Unregistered pin `{pin}`"
    logger.log('check_pin', logger.STATUS_ERROR, error)
    return {
        'success': False,
        'error': error
    }

def check_rfid(rfid):
    '''
    check_rfid(rfid)
    '''
    row_list = retrieve_users({
        'rfid': rfid
    })
    if len(row_list) > 0:
        user_id = row_list[0]['id']
        logger.log('check_rfid', logger.STATUS_SUCCESS, f"id: {user_id}")
        return {
            'success': True
        }
    error = f"Unregistered rfid `{rfid}`"
    logger.log('check_rfid', logger.STATUS_ERROR, error)
    return {
        'success': False,
        'error': error
    }

def check_level(user_id, level, user_id_2=None, level_2=None):
    '''
    check_level(user_id, level, user_id_2=None, level_2=None)
    '''
    row_list = _database_connection.query('SELECT level FROM Users WHERE id = ?;', (user_id, ))
    if len(row_list) > 0:
        user_level = row_list[0]['level']
        if user_level <= level:
            if user_id_2 in (None, user_id):
                logger.log('check_level', logger.STATUS_SUCCESS, f"id: {user_id}")
                return {
                    'success': True
                }
            row_list = _database_connection.query('SELECT level FROM Users WHERE id = ?;', (user_id_2, ))
            if len(row_list) > 0:
                user_level_2 = row_list[0]['level']
                if user_level_2 > user_level and user_level <= level_2:
                    logger.log('check_level', logger.STATUS_SUCCESS, f"id: {user_id} on id: {user_id_2}")
                    return {
                        'success': True
                    }
                error = f"Permission denied for id `{user_id}` on id `{user_id_2}`"
                logger.log('check_level', logger.STATUS_ERROR, error)
                return {
                    'success': False,
                    'error': error
                }
            error = f"Unregistered id `{user_id_2}`"
            logger.log('check_level', logger.STATUS_ERROR, error)
            return {
                'success': False,
                'error': error
            }
        error = f"Permission denied for id `{user_id}`"
        logger.log('check_level', logger.STATUS_ERROR, error)
        return {
            'success': False,
            'error': error
        }
    error = f"Unregistered id `{user_id}`"
    logger.log('check_level', logger.STATUS_ERROR, error)
    return {
        'success': False,
        'error': error
    }

def check_active(username):
    '''
    check_active(username)
    '''
    row_list = _database_connection.query('SELECT active FROM Users WHERE username = ?;', (username, ))
    if len(row_list) > 0:
        active = row_list[0]['active']
        if active:
            logger.log('check_active', logger.STATUS_SUCCESS, f"username: {username}")
            return {
                'success': True
            }
        error = f"Inactive username `{username}`"
        logger.log('check_active', logger.STATUS_ERROR, error)
        return {
            'success': False,
            'error': error
        }
    error = f"Unregisterd username `{username}`"
    logger.log('check_active', logger.STATUS_ERROR, error)
    return {
        'success': False,
        'error': error
    }

################################################################################

def create_session(user_id, token):
    '''
    create_session(user_id, token)
    '''
    if len(_database_connection.query('SELECT * FROM Sessions where id = ?;', (user_id, ))) == 0:
        try:
            _database_connection.query('INSERT INTO Sessions(id, token, expire_datetime) VALUES (?, ?, ?);', (user_id, token, datetime.datetime.now() + datetime.timedelta(seconds=_config['token_expire_seconds']), ))
            logger.log('create_session', logger.STATUS_SUCCESS, f"id: {user_id}")
            return {
                'success': True
            }
        except mariadb.Error as error:
            logger.log('create_session', logger.STATUS_ERROR, str(error))
            return {
                'success': False,
                'error': str(error)
            }
    else:
        return update_session(user_id, token)

def update_session(user_id, token):
    '''
    update_session(user_id, token)
    '''
    try:
        _database_connection.query('UPDATE Sessions SET token = ?, expire_datetime = ? WHERE id = ?;', (token, datetime.datetime.now() + datetime.timedelta(seconds=_config['token_expire_seconds']), user_id, ))
        logger.log('update_session', logger.STATUS_SUCCESS, f"id: {user_id}")
        return {
            'success': True
        }
    except mariadb.Error as error:
        logger.log('update_session', logger.STATUS_ERROR, str(error))
        return {
            'success': False,
            'error': str(error)
        }

def check_token(user_id, token):
    '''
    check_token(user_id, token)
    '''
    row_list = _database_connection.query('SELECT token, expire_datetime FROM Sessions WHERE id = ?;', (user_id, ))
    if len(row_list) > 0:
        stored_token = row_list[0]['token']
        expire_datetime = row_list[0]['expire_datetime']
        if token == stored_token:
            if expire_datetime > datetime.datetime.now():
                new_token = secrets.token_hex()
                response = update_session(user_id, new_token)
                if response['success']:
                    logger.log('check_token', logger.STATUS_SUCCESS, f"id: {user_id}")
                    return {
                        'success': True,
                        'token': new_token
                    }
                logger.log('check_token', logger.STATUS_ERROR, response['error'])
                return {
                    'success': False,
                    'error': response['error']
                }
            error = f"Expired token for id `{user_id}`"
            logger.log('check_token', logger.STATUS_ERROR, error)
            return {
                'success': False,
                'error': error
            }
        error = f"Invalid token for id `{user_id}`"
        logger.log('check_token', logger.STATUS_ERROR, error)
        return {
            'success': False,
            'error': error
        }
    error = f"Token for id `{user_id}` not registered"
    logger.log('check_token', logger.STATUS_ERROR, error)
    return {
        'success': False,
        'error': error
    }
