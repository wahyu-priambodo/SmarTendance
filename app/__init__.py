from flask import Flask
import os

from .extensions import api, db, migrate, cors, jwt
from .config import Config
from .rest.resources import ns

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
  app.config['JWT_TOKEN_LOCATION'] = ['cookies']
  app.config['JWT_COOKIE_SECURE'] = True
  app.config['JWT_COOKIE_HTTPONLY'] = True
  app.config['ERROR_404_HELP'] = False
  
  api.init_app(app)
  
  db.init_app(app)
  migrate.init_app(app, db)
  
  cors.init_app(app)
  jwt.init_app(app)
  
  # # adding resources
  api.add_namespace(ns)
  
  return app