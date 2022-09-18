import mariadb
import json



f = open('config.json', 'r')
config = json.loads(f.read())['database']
f.close()



class Database:
    __config = config

    def __connect():
        return mariadb.connect(user=Database.__config['user'], password=Database.__config['password'], host=Database.__config['host'], port=Database.__config['port'], database=Database.__config['database'])

    def query(query_str, arg_tuple = None):
        connection = Database.__connect()
        cursor = connection.cursor()
        cursor.execute(query_str, arg_tuple)
        row_list = [e for e in cursor]
        connection.close()
        return row_list
