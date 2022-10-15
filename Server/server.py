'''
server.py
'''
import flask

from serverlib import commons
from serverlib import loggerconsole
from serverlib import database
from routers import register
from routers import login
from routers import dashboard
from routers import devices
from routers import users
from routers import proxy



_config = commons.config['server']



api = flask.Flask(__name__)



@api.route('/', methods=['GET'])
@api.route('/index', methods=['GET'])
@api.route('/index.html', methods=['GET'])
def get_index():
    '''
    get_index()
    '''
    return flask.redirect('/login')



@api.route('/assets/<path:path>', methods=['GET'])
def get_asset(path):
    '''
    get_asset(path)
    '''
    return flask.send_from_directory('static', path)



api.register_blueprint(register.router, url_prefix='/register')
api.register_blueprint(login.router, url_prefix='/login')
api.register_blueprint(dashboard.router, url_prefix='/dashboard')
api.register_blueprint(devices.router, url_prefix='/devices')
api.register_blueprint(users.router, url_prefix='/users')
api.register_blueprint(proxy.router, url_prefix='/proxy')



@api.route('/localhost', methods=['GET'])
def get_localhost():
    '''
    get_localhost()
    '''
    return {
        'success': True,
        'data': {
            'boolean': True,
            'number': 1,
            'string': 'prova',
            'list': 'uno',
            'data': {
                'boolean': True,
                'number': 1,
                'string': 'prova',
                'list': 'uno'
            }
        }
    }



@api.route('/localhost', methods=['PATCH'])
def patch_localhost():
    '''
    patch_localhost()
    '''
    return {
        'success': True
    }



@api.route('/localhost/info', methods=['GET'])
def get_localhost_info():
    '''
    get_localhost_info()
    '''
    return {
        'success': True,
        'data': {
            'boolean': 'boolean',
            'number': 'number',
            'string': 'string',
            'list': ['uno','due','tre'],
            'data': {
                'boolean': 'boolean',
                'number': 'number',
                'string': 'string',
                'list': ['uno','due','tre']
            }
        }
    }



if __name__ == '__main__':
    loggerconsole.info('Initialization')
    commons.init_pin_list([user['pin'] for user in database.retrieve_users()])
    loggerconsole.info('Done initialization')
    api.run(host='0.0.0.0', port=_config['port'])
