import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = secrets.token_hex()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False