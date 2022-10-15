'''
register.py
'''
import flask



router = flask.Blueprint('router', __name__)



@router.route('', methods=['GET'])
def get_register():
    '''
    get_register()
    '''
    return flask.send_file('static/html/register.html')
