from server_lib.database import Database



print('LOM initialization')
username = input('username: ')
if not username:
    print('ERROR: username can\'t be empty')
    exit(1)
password = input('password: ')
if not password:
    print('ERROR: password can\'t be empty')
    exit(1)
print(Database.create_user(username, password, Database.user_level_admin, True))
