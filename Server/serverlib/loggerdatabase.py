'''
loggerdatabase.py
'''
from serverlib import commons
from serverlib.databaseconnection import DatabaseConnection



_config = commons.config['loggerdatabase']



_database_connection = DatabaseConnection(_config['database_connection'])



def create_log(operation, status, log):
    '''
    create_log(operation, status, log)
    '''
    if _config['log']:
        _database_connection.query(f"INSERT INTO {_config['table']}(operation, status, log) VALUES (?, ?, ?);", (operation, status, log, ))
