'''
databaseconnection.py
'''
import mariadb

from serverlib import loggerconsole



class DatabaseConnection:
    '''
    DatabaseConnection
    '''
    def __init__(self, config):
        self.__config = config

    def __connect(self):
        '''
        __connect()
        '''
        return mariadb.connect(user=self.__config['user'], password=self.__config['password'], host=self.__config['host'], port=self.__config['port'], database=self.__config['database'], autocommit=self.__config['autocommit'])

    def query(self, query_str, arg_tuple = None):
        '''
        query(query_str, arg_tuple = None)
        '''
        loggerconsole.query(f"query_str: {loggerconsole.orange(query_str)}, arg_tuple: {loggerconsole.orange(str(arg_tuple))}")
        connection = self.__connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query_str, arg_tuple)
        try:
            row_list = list(cursor)
        except mariadb.ProgrammingError:
            row_list = None
        connection.close()
        loggerconsole.query(f"row_list: {loggerconsole.orange(str(row_list))}")
        return row_list
