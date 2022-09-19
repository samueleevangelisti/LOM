import bcrypt
import datetime
import json
import secrets

from .logger import Logger
from .database_core import DatabaseCore



f = open('config.json', 'r')
config = json.loads(f.read())['database']
f.close()



class Database:
    __config = config
    user_level_admin = 0
    user_level_user = 9

    def retrieve_all_users():
        row_list = DatabaseCore.query('SELECT id, level, username, pin IS NOT NULL AS is_pin, rfid IS NOT NULL as is_rfid FROM Users;')
        return [(e[0], e[1], e[2], bool(e[3]), bool(e[4])) for e in row_list]

    def create_user(level, username, password):
        if len(DatabaseCore.query('SELECT * FROM Users WHERE username = ?;', (username, ))) == 0:
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            try:
                DatabaseCore.query('INSERT INTO Users(level, username, password) VALUES (?, ?, ?);', (level, username, password_hash, ))
                Logger.log('create_user', Logger.state_success, 'username: {:s}'.format(username))
                return {
                    'success': True
                }
            except Exception as exception:
                Logger.log('create_user', Logger.state_error, str(exception))
                return {
                    'success': False,
                    'error': str(exception)
                }
        else:
            error = 'Username `{:s}` already exists'.format(username)
            Logger.log('create_user', Logger.state_error, error)
            return {
                'success': False,
                'error': error
            }

    def check_password(username, password):
        row_list = DatabaseCore.query('SELECT id, password FROM Users WHERE username = ?;', (username, ))
        if len(row_list) > 0:
            user_id, password_hash = row_list[0]
            if bcrypt.checkpw(password.encode(), password_hash.encode()):
                Logger.log('check_password', Logger.state_success, 'username: {:s}'.format(username))
                return {
                    'success': True,
                    'id': user_id
                }
            else:
                error = 'Invalid password for username `{:s}`'.format(username)
                Logger.log('check_password', Logger.state_error, error)
                return {
                    'success': False,
                    'error': error
                }
        else:
            error = 'Username `{:s}` not registered'.format(username)
            Logger.log('check_password', Logger.state_error, error)
            return {
                'success': False,
                'error': error
            }

    def check_level(user_id, level):
        row_list = DatabaseCore.query('SELECT level FROM Users WHERE id = ?;', (user_id, ))
        if len(row_list) > 0:
            user_level, = row_list[0]
            if level >= user_level:
                Logger.log('check_level', Logger.state_success, 'id: {:d}'.format(user_id))
                return {
                    'success': True
                }
            else:
                error = 'Permission denied for id {:d}'.format(user_id)
                Logger.log('check_level', Logger.state_error, error)
                return {
                    'success': False,
                    'error': error
                }
        else:
            error = 'Unregistered id {:d}'.format(user_id)
            Logger.log('check_level', Logger.state_error, error)
            return {
                'success': False,
                'error': error
            }

    def create_session(user_id, token):
        if len(DatabaseCore.query('SELECT * FROM Sessions where id = ?;', (user_id, ))) == 0:
            try:
                DatabaseCore.query('INSERT INTO Sessions(id, token, expire_datetime) VALUES (?, ?, ?);', (user_id, token, datetime.datetime.now() + datetime.timedelta(seconds=Database.__config['token_expire_seconds'])))
                Logger.log('create_session', Logger.state_success, 'id: {:d}'.format(user_id))
                return {
                    'success': True
                }
            except Exception as exception:
                Logger.log('create_session', Logger.state_error, str(exception))
                return {
                    'success': False,
                    'error': str(exception)
                }
        else:
            return Database.update_session(user_id, token)

    def update_session(user_id, token):
        try:
            DatabaseCore.query('UPDATE Sessions SET token = ?, expire_datetime = ? WHERE id = ?;', (token, datetime.datetime.now() + datetime.timedelta(seconds=Database.__config['token_expire_seconds']), user_id, ))
            Logger.log('update_session', Logger.state_success, 'id: {:d}'.format(user_id))
            return {
                'success': True
            }
        except Exception as exception:
            Logger.log('update_session', Logger.state_error, str(exception))
            return {
                'success': False,
                'error': str(exception)
            }

    def check_token(user_id, token):
        row_list = DatabaseCore.query('SELECT token, expire_datetime FROM Sessions WHERE id = ?;', (user_id, ))
        if len(row_list) > 0:
            stored_token, expire_datetime = row_list[0]
            if token == stored_token:
                if expire_datetime > datetime.datetime.now():
                    new_token = secrets.token_hex()
                    response = Database.update_session(user_id, new_token)
                    if response['success']:
                        Logger.log('check_token', Logger.state_success, 'id: {:d}'.format(user_id))
                        return {
                            'success': True,
                            'token': new_token
                        }
                    else:
                        Logger.log('check_token', Logger.state_error, response['error'])
                        return {
                            'success': False,
                            'error': response['error']
                        }
                else:
                    error = 'Expired token for {:d}'.format(user_id)
                    Logger.log('check_token', Logger.state_error, error)
                    return {
                        'success': False,
                        'error': error
                    }
            else:
                error = 'Invalid token for {:d}'.format(user_id)
                Logger.log('check_token', Logger.state_error, error)
                return {
                    'success': False,
                    'error': error
                }
        else:
            error = 'Token for {:s} not registered'.format(user_id)
            Logger.log('check_token', Logger.state_error, error)
            return {
                'success': False,
                'error': error
            }
