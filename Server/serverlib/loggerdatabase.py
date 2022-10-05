'''
loggerdatabase.py
'''
import json

from serverlib.databaseconnection import DatabaseConnection



with open('config.json', 'r', encoding='utf-8') as f:
    __config = json.loads(f.read())['loggerdatabase']
    f.close()



database_connection = DatabaseConnection(__config['database_connection'])



def create_log(operation, status, log):
    '''
    create_log(operation, status, log)
    '''
    if __config['log']:
        database_connection.query(f"INSERT INTO {__config['table']}(operation, status, log) VALUES (?, ?, ?);", (operation, status, log, ))
