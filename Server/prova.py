import requests
from database import Database



# try:
#     request = requests.get('http://localhost:8080/companies')
#     print(request.status_code)
#     print(request.json())
# except Exception as exception:
#     print(exception)

print(Database.query('SELECT * FROM Users;'))
