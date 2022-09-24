import mariadb
import json
import datetime



f = open('config.json', 'r')
config = json.loads(f.read())['databaseCore']
f.close()



class DatabaseCore:
    __config = config

    def __connect():
        return mariadb.connect(user=DatabaseCore.__config['user'], password=DatabaseCore.__config['password'], host=DatabaseCore.__config['host'], port=DatabaseCore.__config['port'], database=DatabaseCore.__config['database'], autocommit=DatabaseCore.__config['autocommit'])

    def query(query_str, arg_tuple = None):
        connection = DatabaseCore.__connect()
        cursor = connection.cursor()
        cursor.execute(query_str, arg_tuple)
        try:
            row_list = [e for e in cursor]
        except Exception:
            row_list = None
        connection.close()
        return row_list



class DatabaseLog:
    def create_log(operation, state, log):
        DatabaseCore.query('INSERT INTO Logs(creation_datetime, operation, state, log) VALUES (?, ?, ?, ?)', (datetime.datetime.now(), operation, state, log))
