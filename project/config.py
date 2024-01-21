from dotenv import load_dotenv
from os import path, environ

# Load flask environment variables (.flaskenv)
flaskenv_path = path.join(path.dirname(__file__), '.flaskenv')
load_dotenv(flaskenv_path)

# DbConfig configuration
class DbConfig(object):
  SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_RECORD_QUERIES = True
  SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_timeout": 30,
    "pool_size": 10,
    "max_overflow": 20
  }

# TestingConfig configuration
class TestingConfig(DbConfig):
  DEBUG = True
  TESTING = True
  SECRET_KEY = str(environ.get('SECRET_KEY'))
  ARGON2_HASH_LENGTH = 32
  ARGON2_SALT_LENGTH = 8

# ProductionConfig configuration
class ProductionConfig(DbConfig):
  DEBUG = False
  TESTING = False
  SECRET_KEY = str(environ.get('SECRET_KEY'))
  ARGON2_HASH_LENGTH = 64
  ARGON2_SALT_LENGTH = 16