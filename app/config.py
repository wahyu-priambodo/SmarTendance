import os

from .extensions import db

class Config(object):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_RECORD_QUERIES = True