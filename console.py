'''
generatetables.py
'''
import os
from os import path
import json

from Server.serverlib.databaseconnection import DatabaseConnection



os.chdir(path.dirname(path.realpath(__file__)))



def generate_tables():
    '''
    generate_tables()
    '''
    with open('Server/config.json', 'r', encoding='utf-8') as file:
        config = json.loads(file.read())['database']
        file.close()
    database_connection = DatabaseConnection(config['database_connection'])
    with open('Database/Devices.sql', 'r', encoding='utf-8') as file:
        database_connection.query(file.read())
        file.close()
    with open('Database/Users.sql', 'r', encoding='utf-8') as file:
        database_connection.query(file.read())
        file.close()
    with open('Database/Sessions.sql', 'r', encoding='utf-8') as file:
        database_connection.query(file.read())
        file.close()
    with open('Database/Logs.sql', 'r', encoding='utf-8') as file:
        database_connection.query(file.read())
        file.close()
