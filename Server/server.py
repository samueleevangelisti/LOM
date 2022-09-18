import flask
import json

from logger import Logger



api = flask.Flask(__name__)

@api.route('/companies', methods=['GET'])
def get_companies():
  return json.dumps(companies)

if __name__ == '__main__':
    api.run(port=8080)
