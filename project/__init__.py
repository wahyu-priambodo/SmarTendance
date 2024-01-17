from flask import Flask
from datetime import timedelta

from .config import TestingConfig, ProductionConfig
from .extensions import argon2, db, migrate, csrf
from .app.views import user_ep, admin_ep, lecturer_ep, student_ep

def create_app(testing: bool = True):
  app = Flask(__name__)
  app.permanent_session_lifetime = timedelta(hours=1)
  # Check for testing parameter value.
  if testing:
    app.config.from_object(TestingConfig)
  else:
    app.config.from_object(ProductionConfig)
  # Connecting extensions to flask app
  argon2.init_app(app)
  db.init_app(app)
  migrate.init_app(app, db)
  csrf.init_app(app)
  # Registering route or endpoint blueprints
  app.register_blueprint(user_ep)
  app.register_blueprint(admin_ep)
  app.register_blueprint(lecturer_ep)
  app.register_blueprint(student_ep)
  
  return app