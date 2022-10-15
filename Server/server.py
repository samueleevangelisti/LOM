'''
server.py
'''
import random
import json
import flask

from routers import register, login, dashboard, devices, users, proxy



with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())['server']
    f.close()



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
            'switch1': random.randint(0, 1) == 0
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
            'switch1': 'boolean'
        }
    }



if __name__ == '__main__':
    api.run(host='0.0.0.0', port=config['port'])
