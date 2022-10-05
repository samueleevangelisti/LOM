'''
proxy.py
'''
import json
import flask
import requests

from serverlib import utils



router = flask.Blueprint('proxy', __name__)



@router.route('/', methods=['POST'])
@utils.check_token
def post_proxy():
    '''
    post_proxy()
    '''
    try:
        data_dict = json.loads(flask.request.data.decode())
        if data_dict['method'] == 'GET':
            request = requests.get(data_dict['url'])
            return request.json()
        if data_dict['method'] == 'PATCH':
            request = requests.patch(data_dict['url'], json=data_dict['data'])
            return request.json()
    # pylint: disable-next=broad-except
    except Exception as exception:
        return {
            'success': False,
            'error': str(exception)
        }
    return {
        'success': False,
        'error': f"Unhandled method {data_dict['method']}"
    }
