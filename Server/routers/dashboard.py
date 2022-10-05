'''
dashboard.py
'''
import flask

from serverlib import database, utils



router = flask.Blueprint('dashboard', __name__)



@router.route('/', methods=['GET'])
def get_dashboard():
    '''
    get_dashboard()
    '''
    return flask.send_file('static/html/dashboard.html')



@router.route('/sections', methods=['GET'])
@utils.check_token
def get_dashboard_sections():
    '''
    get_dashboard_sections()
    '''
    user_id = int(flask.request.headers['LOM_id'])
    return {
        'success': True,
        'data': {
            'is_devices': True,
            'is_users': database.check_level(user_id, database.USER_LEVEL_ADMIN)['success']
        }
    }
