import os
from distutils.util import strtobool

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_HOST', '5432')
DB_NAME = 'todo_home'

DATABASE_URL = f'postgresql://postgres:docker@{DB_HOST}:{DB_PORT}/{DB_NAME}'

HOST = str(os.environ.get('HOST', 'localhost'))
PORT = int(os.environ.get('PORT', '5000'))

class Config(object):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', DATABASE_URL)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SERVER_NAME = os.getenv('SERVER_NAME', f'{HOST}:{PORT}')
	DEBUG = strtobool(os.environ.get('DEBUG', 'True'))
	SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')

	if DEBUG:
		ENV = 'development'
		SESSION_COOKIE_DOMAIN = False
