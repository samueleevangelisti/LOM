'''
bootstrap.py
'''
import sys
from serverlib import database



print('LOM initialization')
username = input('username: ')
if not username:
    print('ERROR: username can\'t be empty')
    sys.exit(1)
password = input('password: ')
if not password:
    print('ERROR: password can\'t be empty')
    sys.exit(1)
print(database.create_user(username, password, database.USER_LEVEL_ADMIN, True))
