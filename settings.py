import os

from dotenv import load_dotenv

load_dotenv()
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
invalid_email = os.getenv('invalid_email')
invalid_password = os.getenv('invalid_password')

# Для тестов сразу и невалидный ключ создадим
invalid_auth_key = {'key': 'cdaec06cxxxxxxxx4b133c1922c539a4cc1e7a6135b232e398baf8e3'}